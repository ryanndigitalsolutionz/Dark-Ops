from datetime import datetime, timezone

from sqlalchemy import func

from extensions import db
from models.incident_action import IncidentAction
from .console import CAPABILITIES, DEFAULT_MEMBER_CAPABILITIES


class PermissionError(Exception):
    pass


MAX_DARKOPS_RESPONSE_ATTEMPTS = 2

ALLOWED_NOTIFICATION_CHANNELS = {"in_app", "websocket"}

ALLOWED_ALERT_SEVERITIES = {
    "informational",
    "low",
    "medium",
    "high",
    "critical",
}

ALLOWED_ALERT_STATUSES = {
    "open",
    "acknowledged",
    "investigating",
    "resolved",
    "dismissed",
}

ALLOWED_EXECUTION_MODES = {
    "approval_required",
    "automatic",
}

ALLOWED_TARGET_SCOPES = {
    "application",
    "asset",
    "event",
    "incident",
}


def capability_exists(capability):
    return capability in CAPABILITIES


def validate_capabilities(capabilities):
    if capabilities is None:
        return set()

    if not isinstance(capabilities, (set, list, tuple)):
        raise PermissionError("Capabilities must be a collection.")

    capabilities = set(capabilities)
    unknown = capabilities - CAPABILITIES.keys()

    if unknown:
        raise PermissionError(
            f"Unknown capabilities: {', '.join(sorted(unknown))}"
        )

    return capabilities


def has_capability(capabilities, capability):
    return capability in validate_capabilities(capabilities)


def get_default_member_capabilities():
    return set(DEFAULT_MEMBER_CAPABILITIES)


def validate_capability_assignment(
    assigner_capabilities,
    requested_capabilities,
    is_team_owner=False,
):
    requested = validate_capabilities(requested_capabilities)

    if is_team_owner:
        return requested

    assigner = validate_capabilities(assigner_capabilities)

    if "team.assign_capabilities" not in assigner:
        raise PermissionError(
            "Capability assignment permission is required."
        )

    undelegated = requested - assigner

    if undelegated:
        raise PermissionError(
            "A member cannot delegate capabilities they do not possess."
        )

    return requested


def validate_team_message_recipients(
    active_member_ids,
    recipient_ids=None,
):
    active_member_ids = set(active_member_ids)

    if not recipient_ids:
        return {
            "audience": "all_members",
            "recipient_ids": active_member_ids,
        }

    recipient_ids = set(recipient_ids)
    invalid = recipient_ids - active_member_ids

    if invalid:
        raise PermissionError(
            "Message recipients must be active team members."
        )

    return {
        "audience": "selected_members",
        "recipient_ids": recipient_ids,
    }


def can_view_targeting_trail(capabilities):
    return has_capability(
        capabilities,
        "team_envelope.view_targeting_trail",
    )


def targeting_trail_payload(sender_id, recipient_ids, created_at):
    return {
        "sender_user_id": sender_id,
        "recipient_user_ids": list(recipient_ids),
        "created_at": created_at,
    }


def targeting_trail_exposes_content():
    return False


def can_execute_response(decision, policy):
    if not decision or not policy:
        return False

    if not policy.enabled:
        return False

    if decision.approval_required:
        if decision.approval_status != "approved":
            return False

    return decision.execution_status == "pending"


def can_use_response_policy(policy):
    return bool(
        policy
        and policy.enabled
        and policy.execution_mode in ALLOWED_EXECUTION_MODES
        and policy.target_scope in ALLOWED_TARGET_SCOPES
    )


def get_darkops_response_attempt_count(incident_id):
    return (
        db.session.query(func.count(IncidentAction.id))
        .filter(
            IncidentAction.incident_id == incident_id,
            IncidentAction.attempt_number.isnot(None),
            IncidentAction.triggered_by_user_id.is_(None),
        )
        .scalar()
        or 0
    )


def can_darkops_attempt_response(incident_id):
    return (
        get_darkops_response_attempt_count(incident_id)
        < MAX_DARKOPS_RESPONSE_ATTEMPTS
    )


def get_next_darkops_attempt_number(incident_id):
    attempts = get_darkops_response_attempt_count(incident_id)

    if attempts >= MAX_DARKOPS_RESPONSE_ATTEMPTS:
        raise PermissionError(
            "DarkOps has reached the two-response-attempt limit."
        )

    return attempts + 1


def enforce_darkops_response_attempt(incident_id):
    attempt_number = get_next_darkops_attempt_number(incident_id)

    if attempt_number > MAX_DARKOPS_RESPONSE_ATTEMPTS:
        raise PermissionError(
            "DarkOps cannot perform another automated response attempt."
        )

    return attempt_number


def customer_remediation_allowed():
    return True


def response_hold_required(incident_id):
    return (
        get_darkops_response_attempt_count(incident_id)
        >= MAX_DARKOPS_RESPONSE_ATTEMPTS
    )


def utcnow():
    return datetime.now(timezone.utc)
