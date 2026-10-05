from datetime import datetime, timezone

from flask import current_app

from models.application import Application
from models.alert import Alert
from models.audit_log import AuditLog
from models.incident import Incident
from models.notification import Notification
from models.team_member import TeamMember
from models.user import User


class ExtensionError(Exception):
    pass


DESTINATIONS = [
    {"key": "dashboard", "label": "Dashboard", "description": "Main DarkOps dashboard", "aliases": ["home", "main page", "overview"]},
    {"key": "profile", "label": "My Profile", "description": "View and manage your profile", "aliases": ["account", "me", "user profile"]},
    {"key": "applications", "label": "Applications", "description": "Protected applications", "aliases": ["apps", "my apps", "protected apps", "secure my app"]},
    {"key": "assets", "label": "Assets", "description": "Application security assets", "aliases": ["security assets"]},
    {"key": "events", "label": "Security Events", "description": "Security events received by DarkOps", "aliases": ["events", "activity"]},
    {"key": "alerts", "label": "Alerts", "description": "Security alerts", "aliases": ["security alerts", "warnings"]},
    {"key": "incidents", "label": "Incidents", "description": "Security incidents", "aliases": ["security incidents", "cases"]},
    {"key": "vulnerabilities", "label": "Vulnerabilities", "description": "Application vulnerabilities", "aliases": ["vulns", "security vulnerabilities"]},
    {"key": "response", "label": "Response", "description": "Response decisions and actions", "aliases": ["respond", "response actions"]},
    {"key": "recovery", "label": "Recovery", "description": "Recovery operations", "aliases": ["recover", "recovery operations"]},
    {"key": "notifications", "label": "Notifications", "description": "Your DarkOps notifications", "aliases": ["alerts inbox", "messages"]},
    {"key": "teams", "label": "Teams", "description": "Team membership and administration", "aliases": ["team", "members", "team members"]},
    {"key": "api_keys", "label": "API Keys", "description": "DarkOps API keys and Duo Dev access", "aliases": ["keys", "duo dev", "developer keys"]},
    {"key": "subscriptions", "label": "Subscriptions", "description": "Subscription and billing settings", "aliases": ["plan", "billing", "subscription"]},
    {"key": "settings", "label": "Settings", "description": "DarkOps settings", "aliases": ["preferences", "configuration"]},
    {"key": "trust", "label": "Trust Center", "description": "Security trust information", "aliases": ["trust", "security trust"]},
    {"key": "intelligence", "label": "Intelligence", "description": "Security intelligence and enrichment", "aliases": ["threat intelligence", "intel"]},
    {"key": "agents", "label": "Agents", "description": "DarkOps security agents and automation", "aliases": ["automation", "security agents"]},
]


def _utcnow():
    return datetime.now(timezone.utc)


def _get_user(user):
    if not user:
        raise ExtensionError("Authenticated user is required.")

    if not isinstance(user, User):
        raise ExtensionError("Invalid authenticated user.")

    if user.status != "active":
        raise ExtensionError("User account is not active.")

    return user


def _get_team_ids(user_id):
    memberships = TeamMember.query.filter_by(
        user_id=user_id,
        status="active",
    ).all()

    return [membership.team_id for membership in memberships]


def _get_application_ids(user):
    team_ids = _get_team_ids(user.id)

    query = Application.query.filter(
        (Application.owner_user_id == user.id)
    )

    applications = query.all()

    if team_ids:
        team_applications = Application.query.filter(
            Application.team_id.in_(team_ids)
        ).all()

        applications.extend(team_applications)

    return list({application.id for application in applications})


def get_extension_identity(user):
    user = _get_user(user)

    return {
        "user_id": user.id,
        "darkops_id": user.darkops_id,
        "username": user.username,
        "email": user.email,
        "status": user.status,
        "last_login_at": user.last_login_at,
    }


def get_extension_presence(user, session=None):
    user = _get_user(user)

    if not session:
        return {
            "authenticated": True,
            "present": True,
            "session_id": None,
            "last_seen_at": None,
        }

    return {
        "authenticated": True,
        "present": session.status == "active",
        "session_id": session.id,
        "last_seen_at": session.last_seen_at,
        "expires_at": session.expires_at,
    }


def get_extension_summary(user):
    user = _get_user(user)
    application_ids = _get_application_ids(user)

    application_query = Application.query.filter(
        Application.id.in_(application_ids)
    ) if application_ids else Application.query.filter(False)

    applications = application_query.all()

    alerts = Alert.query.filter(
        Alert.application_id.in_(application_ids),
        Alert.status.in_(["open", "investigating"]),
    ).count() if application_ids else 0

    incidents = Incident.query.filter(
        Incident.application_id.in_(application_ids),
        Incident.status.in_(["open", "investigating", "contained"]),
    ).count() if application_ids else 0

    vulnerabilities = 0

    try:
        from models.vulnerability import Vulnerability

        vulnerabilities = Vulnerability.query.filter(
            Vulnerability.application_id.in_(application_ids),
            Vulnerability.status.in_(["open", "acknowledged", "resolving"]),
        ).count() if application_ids else 0
    except ImportError:
        vulnerabilities = 0

    unread_notifications = Notification.query.filter(
        Notification.user_id == user.id,
        Notification.status == "unread",
    ).count()

    return {
        "applications": {
            "total": len(applications),
            "connected": sum(
                1 for application in applications
                if application.status == "connected"
            ),
        },
        "alerts": alerts,
        "incidents": incidents,
        "vulnerabilities": vulnerabilities,
        "unread_notifications": unread_notifications,
    }


def get_extension_notifications(user, limit=10):
    user = _get_user(user)

    limit = max(1, min(limit, 50))

    notifications = Notification.query.filter(
        Notification.user_id == user.id
    ).order_by(
        Notification.created_at.desc()
    ).limit(limit).all()

    return notifications


def get_extension_alerts(user, limit=10):
    user = _get_user(user)
    application_ids = _get_application_ids(user)

    if not application_ids:
        return []

    limit = max(1, min(limit, 50))

    return Alert.query.filter(
        Alert.application_id.in_(application_ids)
    ).order_by(
        Alert.created_at.desc()
    ).limit(limit).all()


def get_extension_incidents(user, limit=10):
    user = _get_user(user)
    application_ids = _get_application_ids(user)

    if not application_ids:
        return []

    limit = max(1, min(limit, 50))

    return Incident.query.filter(
        Incident.application_id.in_(application_ids)
    ).order_by(
        Incident.opened_at.desc()
    ).limit(limit).all()


def get_extension_audit_activity(user, limit=20):
    user = _get_user(user)
    application_ids = _get_application_ids(user)

    limit = max(1, min(limit, 100))

    filters = [
        AuditLog.user_id == user.id,
    ]

    if application_ids:
        filters.append(
            AuditLog.application_id.in_(application_ids)
        )

    from sqlalchemy import or_

    logs = AuditLog.query.filter(
        or_(*filters)
    ).order_by(
        AuditLog.occurred_at.desc()
    ).limit(limit).all()

    return logs


def get_extension_security_feed(user, limit=20):
    user = _get_user(user)

    alerts = get_extension_alerts(user, limit)
    incidents = get_extension_incidents(user, limit)
    notifications = get_extension_notifications(user, limit)
    audit_logs = get_extension_audit_activity(user, limit)

    feed = []

    for alert in alerts:
        feed.append({
            "type": "alert",
            "id": alert.id,
            "title": alert.title,
            "description": alert.description,
            "severity": alert.severity,
            "status": alert.status,
            "created_at": alert.created_at,
        })

    for incident in incidents:
        feed.append({
            "type": "incident",
            "id": incident.id,
            "title": incident.title,
            "description": incident.description,
            "severity": incident.severity,
            "status": incident.status,
            "created_at": incident.opened_at,
        })

    for notification in notifications:
        feed.append({
            "type": "notification",
            "id": notification.id,
            "title": notification.title,
            "description": notification.message,
            "severity": None,
            "status": notification.status,
            "created_at": notification.created_at,
        })

    for audit_log in audit_logs:
        feed.append({
            "type": "audit",
            "id": audit_log.id,
            "title": audit_log.action,
            "description": audit_log.resource_type,
            "severity": None,
            "status": "recorded",
            "created_at": audit_log.occurred_at,
        })

    feed.sort(
        key=lambda item: item["created_at"] or _utcnow(),
        reverse=True,
    )

    return feed[:max(1, min(limit, 100))]


def search_extension_destinations(query, limit=5):
    if not query or not isinstance(query, str):
        return []

    normalized_query = query.strip().lower()

    if not normalized_query:
        return []

    limit = max(1, min(limit, 20))
    matches = []

    for destination in DESTINATIONS:
        haystack = " ".join([
            destination["key"],
            destination["label"],
            destination["description"],
            " ".join(destination["aliases"]),
        ]).lower()

        if normalized_query in haystack:
            score = 100 if normalized_query == destination["key"] else 50

            if normalized_query == destination["label"].lower():
                score += 25

            matches.append({
                **destination,
                "score": score,
            })

    matches.sort(
        key=lambda item: (-item["score"], item["label"])
    )

    return matches[:limit]


def get_extension_actions():
    return [
        {
            "key": "return_to_main",
            "label": "Return to Main Page",
            "destination": "dashboard",
        },
        {
            "key": "show_profile",
            "label": "Show my Profile",
            "destination": "profile",
        },
        {
            "key": "secure_app",
            "label": "Secure my App",
            "destination": "applications",
        },
    ]


def get_extension_snapshot(user, session=None):
    user = _get_user(user)

    return {
        "extension": {
            "name": current_app.config.get(
                "DARKOPS_EXTENSION_NAME",
                "DarkOps Extension",
            ),
            "version": current_app.config.get(
                "DARKOPS_EXTENSION_VERSION",
                "1.0.0",
            ),
            "available": True,
        },
        "identity": get_extension_identity(user),
        "presence": get_extension_presence(user, session),
        "summary": get_extension_summary(user),
        "security_feed": get_extension_security_feed(user, 20),
        "actions": get_extension_actions(),
        "generated_at": _utcnow(),
    }


def build_extension_event(event_type, payload):
    if not event_type:
        raise ExtensionError("Extension event type is required.")

    if payload is None:
        payload = {}

    return {
        "type": event_type,
        "payload": payload,
        "generated_at": _utcnow(),
    }
