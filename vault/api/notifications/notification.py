from datetime import datetime, timezone

from extensions import db
from models.notification import Notification

from notifications.ringtone import get_ringtone, ringtone_exists
from notifications.text_action import get_text_action, text_action_exists
from services.websocket import emit_notification


NOTIFICATION_TYPES = {
    "security_alert",
    "event",
    "incident",
    "vulnerability",
    "payment",
    "announcement",
    "system",
    "team",
    "authentication",
}

NOTIFICATION_STATUSES = {
    "unread",
    "read",
}


class NotificationError(Exception):
    pass


def _utcnow():
    return datetime.now(timezone.utc)


def _validate_type(notification_type):
    if notification_type not in NOTIFICATION_TYPES:
        raise NotificationError(
            f"Unknown notification type: {notification_type}"
        )


def _validate_status(status):
    if status not in NOTIFICATION_STATUSES:
        raise NotificationError(
            f"Unknown notification status: {status}"
        )


def _build_metadata(
    metadata=None,
    sound_key=None,
    action_key=None,
):
    payload = dict(metadata or {})

    if sound_key:
        if not ringtone_exists(sound_key):
            raise NotificationError(
                f"Unknown ringtone: {sound_key}"
            )

        payload["sound"] = get_ringtone(sound_key)

    if action_key:
        if not text_action_exists(action_key):
            raise NotificationError(
                f"Unknown text action: {action_key}"
            )

        payload["action"] = get_text_action(action_key)

    return payload


def _notification_payload(notification):
    return {
        "id": notification.id,
        "user_id": notification.user_id,
        "team_id": notification.team_id,
        "sender_user_id": notification.sender_user_id,
        "event_id": notification.event_id,
        "alert_id": notification.alert_id,
        "incident_id": notification.incident_id,
        "vulnerability_id": notification.vulnerability_id,
        "type": notification.type,
        "status": notification.status,
        "title": notification.title,
        "message": notification.message,
        "action_url": notification.action_url,
        "metadata": notification.metadata or {},
        "created_at": notification.created_at,
        "read_at": notification.read_at,
    }


def create_notification(
    user_id,
    notification_type,
    title,
    message,
    *,
    team_id=None,
    sender_user_id=None,
    event_id=None,
    alert_id=None,
    incident_id=None,
    vulnerability_id=None,
    action_url=None,
    metadata=None,
    sound_key=None,
    action_key=None,
    realtime=True,
):
    if not user_id:
        raise NotificationError(
            "Notification recipient is required."
        )

    if not title or not title.strip():
        raise NotificationError(
            "Notification title is required."
        )

    if not message or not message.strip():
        raise NotificationError(
            "Notification message is required."
        )

    _validate_type(notification_type)

    notification = Notification(
        user_id=user_id,
        team_id=team_id,
        sender_user_id=sender_user_id,
        event_id=event_id,
        alert_id=alert_id,
        incident_id=incident_id,
        vulnerability_id=vulnerability_id,
        type=notification_type,
        status="unread",
        title=title.strip(),
        message=message.strip(),
        action_url=action_url,
        metadata=_build_metadata(
            metadata=metadata,
            sound_key=sound_key,
            action_key=action_key,
        ),
        created_at=_utcnow(),
    )

    db.session.add(notification)
    db.session.flush()

    payload = _notification_payload(notification)

    if realtime:
        emit_notification(
            user_id=user_id,
            payload=payload,
        )

    return notification


def create_notifications(
    user_ids,
    notification_type,
    title,
    message,
    **kwargs,
):
    if not user_ids:
        raise NotificationError(
            "At least one notification recipient is required."
        )

    unique_user_ids = list(dict.fromkeys(user_ids))
    notifications = []

    for user_id in unique_user_ids:
        notifications.append(
            create_notification(
                user_id=user_id,
                notification_type=notification_type,
                title=title,
                message=message,
                **kwargs,
            )
        )

    return notifications


def mark_read(notification):
    if not notification:
        raise NotificationError(
            "Notification is required."
        )

    if notification.status == "read":
        return notification

    notification.status = "read"
    notification.read_at = _utcnow()

    db.session.flush()

    return notification


def mark_unread(notification):
    if not notification:
        raise NotificationError(
            "Notification is required."
        )

    notification.status = "unread"
    notification.read_at = None

    db.session.flush()

    return notification


def mark_all_read(user_id):
    if not user_id:
        raise NotificationError(
            "Notification recipient is required."
        )

    now = _utcnow()

    count = Notification.query.filter(
        Notification.user_id == user_id,
        Notification.status == "unread",
    ).update(
        {
            "status": "read",
            "read_at": now,
        },
        synchronize_session=False,
    )

    db.session.flush()

    return count


def delete_notification(notification):
    if not notification:
        raise NotificationError(
            "Notification is required."
        )

    db.session.delete(notification)
    db.session.flush()

    return True


def get_notification_payload(notification):
    if not notification:
        raise NotificationError(
            "Notification is required."
        )

    return _notification_payload(notification)
