from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from models.application import Application
from models.team_member import TeamMember
from models.team_owner import TeamOwner
from models.user import User

from .console import CAPABILITIES, capability_exists
from .permissions import has_capability


class AuthorizationError(Exception):
    pass


WEEKDAYS = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)


def _active_user(user):
    return bool(
        user
        and isinstance(user, User)
        and user.status == "active"
    )


def _team_owner(team_id, user_id):
    return TeamOwner.query.filter_by(
        team_id=team_id,
        user_id=user_id,
        status="active",
    ).first()


def _team_membership(team_id, user_id):
    return TeamMember.query.filter_by(
        team_id=team_id,
        user_id=user_id,
        status="active",
    ).first()


def is_team_owner(team_id, user_id):
    return bool(_team_owner(team_id, user_id))


def is_active_team_member(team_id, user_id):
    return bool(_team_membership(team_id, user_id))


def get_member_capabilities(team_id, user_id):
    if is_team_owner(team_id, user_id):
        return set(CAPABILITIES.keys())

    membership = _team_membership(team_id, user_id)

    if not membership or not membership.role:
        return set()

    permissions = membership.role.permissions

    if isinstance(permissions, dict):
        return {
            key for key, enabled in permissions.items()
            if enabled and capability_exists(key)
        }

    if isinstance(permissions, (list, set, tuple)):
        return {
            key for key in permissions
            if capability_exists(key)
        }

    return set()


def _parse_time(value):
    try:
        hour, minute = value.split(":")
        hour = int(hour)
        minute = int(minute)

        if not 0 <= hour <= 23 or not 0 <= minute <= 59:
            return None

        return hour, minute
    except (AttributeError, ValueError):
        return None


def validate_access_schedule(schedule):
    if schedule is None:
        return True

    if not isinstance(schedule, dict):
        return False

    timezone_name = schedule.get("timezone")

    if not timezone_name:
        return False

    try:
        ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        return False

    for day in WEEKDAYS:
        periods = schedule.get(day, [])

        if periods is None:
            continue

        if not isinstance(periods, list):
            return False

        for period in periods:
            if (
                not isinstance(period, (list, tuple))
                or len(period) != 2
            ):
                return False

            start = _parse_time(period[0])
            end = _parse_time(period[1])

            if not start or not end:
                return False

            if start >= end:
                return False

    return True


def is_within_access_schedule(
    membership,
    now=None,
):
    schedule = membership.access_schedule

    if not schedule:
        return True

    if not validate_access_schedule(schedule):
        return False

    try:
        local_zone = ZoneInfo(schedule["timezone"])
    except ZoneInfoNotFoundError:
        return False

    now = now or datetime.now(timezone.utc)
    local_now = now.astimezone(local_zone)

    day = WEEKDAYS[local_now.weekday()]
    periods = schedule.get(day, [])

    if not periods:
        return False

    current_minutes = (
        local_now.hour * 60
        + local_now.minute
    )

    for start, end in periods:
        start_hour, start_minute = _parse_time(start)
        end_hour, end_minute = _parse_time(end)

        start_minutes = start_hour * 60 + start_minute
        end_minutes = end_hour * 60 + end_minute

        if start_minutes <= current_minutes < end_minutes:
            return True

    return False


def has_team_access(
    team_id,
    user_id,
    now=None,
):
    user = User.query.get(user_id)

    if not _active_user(user):
        return False

    if is_team_owner(team_id, user_id):
        return True

    membership = _team_membership(team_id, user_id)

    if not membership:
        return False

    if membership.status != "active":
        return False

    if not membership.team_access_enabled:
        disabled_until = membership.team_access_disabled_until

        if not disabled_until:
            return False

        now = now or datetime.now(timezone.utc)

        if now < disabled_until:
            return False

    return is_within_access_schedule(
        membership,
        now=now,
    )


def can_access_team(team_id, user_id, now=None):
    return has_team_access(
        team_id,
        user_id,
        now=now,
    )


def can_access_application(
    application,
    user_id,
    capability=None,
    now=None,
):
    if not application:
        return False

    user = User.query.get(user_id)

    if not _active_user(user):
        return False

    if application.owner_user_id == user_id:
        return True

    if not application.team_id:
        return False

    if not has_team_access(
        application.team_id,
        user_id,
        now=now,
    ):
        return False

    if capability:
        return has_user_capability(
            application.team_id,
            user_id,
            capability,
        )

    return True


def has_user_capability(
    team_id,
    user_id,
    capability,
):
    if not capability_exists(capability):
        return False

    if not has_team_access(team_id, user_id):
        return False

    capabilities = get_member_capabilities(
        team_id,
        user_id,
    )

    return has_capability(
        capabilities,
        capability,
    )


def authorize(
    user_id,
    capability,
    team_id=None,
    application=None,
    now=None,
):
    user = User.query.get(user_id)

    if not _active_user(user):
        return False

    if not capability_exists(capability):
        return False

    if application is not None:
        if application.team_id:
            team_id = application.team_id

            if not can_access_application(
                application,
                user_id,
                capability=capability,
                now=now,
            ):
                return False

            return True

        return application.owner_user_id == user_id

    if not team_id:
        return False

    return has_user_capability(
        team_id,
        user_id,
        capability,
    )


def can_manage_member_access(team_id, user_id):
    return is_team_owner(
        team_id,
        user_id,
    ) or has_user_capability(
        team_id,
        user_id,
        "team.manage_member_access",
    )


def can_manage_access_schedule(team_id, user_id):
    return is_team_owner(
        team_id,
        user_id,
    ) or has_user_capability(
        team_id,
        user_id,
        "team.manage_access_schedule",
    )


def can_assign_capabilities(team_id, user_id):
    return is_team_owner(
        team_id,
        user_id,
    ) or has_user_capability(
        team_id,
        user_id,
        "team.assign_capabilities",
    )


def can_view_targeting_trail(team_id, user_id):
    return is_team_owner(
        team_id,
        user_id,
    ) or has_user_capability(
        team_id,
        user_id,
        "team_envelope.view_targeting_trail",
    )


def require_authorization(
    user_id,
    capability,
    team_id=None,
    application=None,
    now=None,
):
    if not authorize(
        user_id=user_id,
        capability=capability,
        team_id=team_id,
        application=application,
        now=now,
    ):
        raise AuthorizationError(
            f"Authorization denied for capability: {capability}"
        )

    return True
