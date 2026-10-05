import os

from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room

from models.session import Session
from models.team_member import TeamMember
from models.team_owner import TeamOwner
from models.user import User

from api.authentication.authentication import authenticate_session
from api.security.authorization import has_team_access


socketio = SocketIO()


class WebSocketServiceError(Exception):
    pass


DEFAULT_NAMESPACE = "/"
TEAM_ROOM_PREFIX = "team:"
USER_ROOM_PREFIX = "user:"
SUPPORT_ROOM_PREFIX = "support:"

ALLOWED_EVENTS = {
    "team_message",
    "support_message",
    "notification",
    "message_read",
    "typing_started",
    "typing_stopped",
    "presence",
}


def init_websocket(app):
    redis_url = (
        app.config.get("SOCKETIO_REDIS_URL")
        or os.getenv(
            "SOCKETIO_REDIS_URL",
            "redis://localhost:6379/0",
        )
    )

    allowed_origins = (
        app.config.get("SOCKETIO_ALLOWED_ORIGINS")
        or os.getenv(
            "SOCKETIO_ALLOWED_ORIGINS",
            "*",
        )
    )

    if isinstance(allowed_origins, str):
        allowed_origins = [
            origin.strip()
            for origin in allowed_origins.split(",")
            if origin.strip()
        ]

    socketio.init_app(
        app,
        cors_allowed_origins=allowed_origins,
        message_queue=redis_url,
        async_mode=app.config.get("SOCKETIO_ASYNC_MODE"),
    )

    return socketio


def _room(prefix, identifier):
    return f"{prefix}{identifier}"


def team_room(team_id):
    return _room(TEAM_ROOM_PREFIX, team_id)


def user_room(user_id):
    return _room(USER_ROOM_PREFIX, user_id)


def support_room(user_id):
    return _room(SUPPORT_ROOM_PREFIX, user_id)


def _get_socket_user():
    session_data = socketio.get_session(
        request.sid,
        namespace=DEFAULT_NAMESPACE,
    )

    if not session_data:
        return None

    user_id = session_data.get("user_id")

    if not user_id:
        return None

    return db_user(user_id)


def db_user(user_id):
    return User.query.get(user_id)


def _authenticate_socket(auth):
    raw_session_token = None

    if isinstance(auth, dict):
        raw_session_token = auth.get("session_token")

    user = authenticate_session(
        raw_session_token=raw_session_token,
        touch=True,
    )

    return user


def _get_user_team_ids(user_id):
    member_team_ids = {
        membership.team_id
        for membership in TeamMember.query.filter_by(
            user_id=user_id,
            status="active",
        ).all()
    }

    owner_team_ids = {
        owner.team_id
        for owner in TeamOwner.query.filter_by(
            user_id=user_id,
            status="active",
        ).all()
    }

    return member_team_ids | owner_team_ids


def _join_user_rooms(user_id):
    join_room(
        user_room(user_id),
        namespace=DEFAULT_NAMESPACE,
    )

    join_room(
        support_room(user_id),
        namespace=DEFAULT_NAMESPACE,
    )

    for team_id in _get_user_team_ids(user_id):
        if has_team_access(team_id, user_id):
            join_room(
                team_room(team_id),
                namespace=DEFAULT_NAMESPACE,
            )


def _leave_user_rooms(user_id):
    leave_room(
        user_room(user_id),
        namespace=DEFAULT_NAMESPACE,
    )

    leave_room(
        support_room(user_id),
        namespace=DEFAULT_NAMESPACE,
    )

    for team_id in _get_user_team_ids(user_id):
        leave_room(
            team_room(team_id),
            namespace=DEFAULT_NAMESPACE,
        )


def _presence_payload(user, status):
    return {
        "user_id": user.id,
        "darkops_id": user.darkops_id,
        "username": user.username,
        "status": status,
    }


def emit_to_user(user_id, event, data):
    if event not in ALLOWED_EVENTS:
        raise WebSocketServiceError(
            f"Unsupported WebSocket event: {event}"
        )

    socketio.emit(
        event,
        data,
        room=user_room(user_id),
        namespace=DEFAULT_NAMESPACE,
    )


def emit_to_team(team_id, event, data, skip_sid=None):
    if event not in ALLOWED_EVENTS:
        raise WebSocketServiceError(
            f"Unsupported WebSocket event: {event}"
        )

    socketio.emit(
        event,
        data,
        room=team_room(team_id),
        skip_sid=skip_sid,
        namespace=DEFAULT_NAMESPACE,
    )


def emit_to_support(user_id, event, data):
    if event not in ALLOWED_EVENTS:
        raise WebSocketServiceError(
            f"Unsupported WebSocket event: {event}"
        )

    socketio.emit(
        event,
        data,
        room=support_room(user_id),
        namespace=DEFAULT_NAMESPACE,
    )


def emit_targeted_message(
    recipient_user_ids,
    data,
    skip_user_id=None,
):
    for user_id in set(recipient_user_ids or []):
        if (
            skip_user_id
            and user_id == skip_user_id
        ):
            continue

        emit_to_user(
            user_id,
            "team_message",
            data,
        )


def emit_team_message(
    team_id,
    data,
    skip_sid=None,
):
    emit_to_team(
        team_id,
        "team_message",
        data,
        skip_sid=skip_sid,
    )


def emit_notification(user_id, data):
    emit_to_user(
        user_id,
        "notification",
        data,
    )


def emit_support_message(user_id, data):
    emit_to_support(
        user_id,
        "support_message",
        data,
    )


def emit_message_read(
    recipient_user_ids,
    data,
):
    for user_id in set(recipient_user_ids or []):
        emit_to_user(
            user_id,
            "message_read",
            data,
        )


def emit_presence(
    team_id,
    user_id,
    status,
):
    user = db_user(user_id)

    if not user:
        return

    emit_to_team(
        team_id,
        "presence",
        _presence_payload(
            user,
            status,
        ),
    )


@socketio.on("connect")
def handle_connect(auth=None):
    user = _authenticate_socket(auth)

    if not user:
        return False

    socketio.save_session(
        request.sid,
        {
            "user_id": user.id,
            "username": user.username,
        },
        namespace=DEFAULT_NAMESPACE,
    )

    _join_user_rooms(user.id)

    for team_id in _get_user_team_ids(user.id):
        if has_team_access(team_id, user.id):
            emit_presence(
                team_id,
                user.id,
                "online",
            )

    emit(
        "connection_ready",
        {
            "authenticated": True,
            "user_id": user.id,
            "darkops_id": user.darkops_id,
        },
    )


@socketio.on("disconnect")
def handle_disconnect():
    session_data = socketio.get_session(
        request.sid,
        namespace=DEFAULT_NAMESPACE,
    )

    if not session_data:
        return

    user_id = session_data.get("user_id")

    if not user_id:
        return

    for team_id in _get_user_team_ids(user_id):
        if has_team_access(team_id, user_id):
            emit_presence(
                team_id,
                user_id,
                "offline",
            )


@socketio.on("team_join")
def handle_team_join(data):
    user = _get_socket_user()

    if not user:
        return {
            "ok": False,
            "error": "Authentication required.",
        }

    team_id = (
        data.get("team_id")
        if isinstance(data, dict)
        else None
    )

    if not team_id:
        return {
            "ok": False,
            "error": "Team ID is required.",
        }

    if not has_team_access(
        team_id,
        user.id,
    ):
        return {
            "ok": False,
            "error": "Team access denied.",
        }

    join_room(
        team_room(team_id),
        namespace=DEFAULT_NAMESPACE,
    )

    return {
        "ok": True,
        "team_id": team_id,
    }


@socketio.on("team_leave")
def handle_team_leave(data):
    user = _get_socket_user()

    if not user:
        return {
            "ok": False,
            "error": "Authentication required.",
        }

    team_id = (
        data.get("team_id")
        if isinstance(data, dict)
        else None
    )

    if not team_id:
        return {
            "ok": False,
            "error": "Team ID is required.",
        }

    leave_room(
        team_room(team_id),
        namespace=DEFAULT_NAMESPACE,
    )

    return {
        "ok": True,
        "team_id": team_id,
    }


@socketio.on("typing_start")
def handle_typing_start(data):
    user = _get_socket_user()

    if not user:
        return

    team_id = (
        data.get("team_id")
        if isinstance(data, dict)
        else None
    )

    if not team_id or not has_team_access(
        team_id,
        user.id,
    ):
        return

    emit_to_team(
        team_id,
        "typing_started",
        {
            "team_id": team_id,
            "user_id": user.id,
            "username": user.username,
        },
        skip_sid=request.sid,
    )


@socketio.on("typing_stop")
def handle_typing_stop(data):
    user = _get_socket_user()

    if not user:
        return

    team_id = (
        data.get("team_id")
        if isinstance(data, dict)
        else None
    )

    if not team_id or not has_team_access(
        team_id,
        user.id,
    ):
        return

    emit_to_team(
        team_id,
        "typing_stopped",
        {
            "team_id": team_id,
            "user_id": user.id,
        },
        skip_sid=request.sid,
    )
