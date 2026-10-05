import hashlib
import json
import secrets
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone

from flask import current_app, g, request
from sqlalchemy import or_
from werkzeug.security import check_password_hash

from extensions import db
from models.session import Session
from models.user import User


class AuthenticationError(Exception):
    pass


class TurnstileVerificationError(AuthenticationError):
    pass


def _utcnow():
    return datetime.now(timezone.utc)


def _hash_token(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _request_ip():
    forwarded_for = request.headers.get("X-Forwarded-For")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.remote_addr


def _request_user_agent():
    return request.headers.get("User-Agent")


def _validate_user(user):
    if not user:
        return None

    if user.status != "active":
        return None

    return user


def _find_user(identifier):
    return User.query.filter(
        or_(
            User.email == identifier,
            User.username == identifier,
        )
    ).first()


def verify_turnstile(token, remote_ip=None, expected_action=None, expected_hostname=None):
    if not token or not isinstance(token, str) or len(token) > 2048:
        raise TurnstileVerificationError("Invalid Turnstile token.")

    secret = current_app.config.get("TURNSTILE_SECRET_KEY")

    if not secret:
        raise TurnstileVerificationError("Turnstile is not configured.")

    payload = {
        "secret": secret,
        "response": token,
        "idempotency_key": str(uuid.uuid4()),
    }

    ip = remote_ip or _request_ip()

    if ip:
        payload["remoteip"] = ip

    body = json.dumps(payload).encode("utf-8")

    siteverify_request = urllib.request.Request(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(siteverify_request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        raise TurnstileVerificationError("Turnstile verification failed.")

    if not result.get("success"):
        raise TurnstileVerificationError("Turnstile verification was rejected.")

    if expected_action and result.get("action") != expected_action:
        raise TurnstileVerificationError("Turnstile action validation failed.")

    if expected_hostname and result.get("hostname") != expected_hostname:
        raise TurnstileVerificationError("Turnstile hostname validation failed.")

    return result


def verify_login_challenge(turnstile_token):
    return verify_turnstile(
        token=turnstile_token,
        expected_action=current_app.config.get("TURNSTILE_LOGIN_ACTION"),
        expected_hostname=current_app.config.get("TURNSTILE_HOSTNAME"),
    )


def verify_registration_challenge(turnstile_token):
    return verify_turnstile(
        token=turnstile_token,
        expected_action=current_app.config.get("TURNSTILE_REGISTRATION_ACTION"),
        expected_hostname=current_app.config.get("TURNSTILE_HOSTNAME"),
    )


def verify_session_resume_challenge(turnstile_token):
    return verify_turnstile(
        token=turnstile_token,
        expected_action=current_app.config.get("TURNSTILE_SESSION_ACTION"),
        expected_hostname=current_app.config.get("TURNSTILE_HOSTNAME"),
    )


def authenticate_credentials(identifier, password, turnstile_token=None):
    if turnstile_token is not None:
        verify_login_challenge(turnstile_token)

    user = _find_user(identifier)

    if not _validate_user(user):
        return None

    if not user.password_hash:
        return None

    if not check_password_hash(user.password_hash, password):
        return None

    user.last_login_at = _utcnow()
    db.session.commit()

    return user


def create_session(
    user,
    expires_at,
    remember_device=False,
    ip_address=None,
    user_agent=None,
    revoke_existing_sessions=True,
):
    if not user:
        raise AuthenticationError("Authenticated user is required.")

    if user.status != "active":
        raise AuthenticationError("User account is not active.")

    if expires_at <= _utcnow():
        raise AuthenticationError("Session expiration must be in the future.")

    if revoke_existing_sessions:
        revoke_other_sessions(user)

    raw_session_token = secrets.token_urlsafe(48)
    now = _utcnow()

    session = Session(
        user_id=user.id,
        session_token_hash=_hash_token(raw_session_token),
        status="active",
        ip_address=ip_address or _request_ip(),
        user_agent=user_agent or _request_user_agent(),
        created_at=now,
        last_seen_at=now,
        expires_at=expires_at,
    )

    db.session.add(session)
    db.session.commit()

    return session, raw_session_token


def create_authenticated_session(user, remember_device=False):
    if remember_device:
        lifetime = current_app.config.get(
            "DARKOPS_REMEMBER_DEVICE_SECONDS",
            2592000,
        )
    else:
        lifetime = current_app.config.get(
            "DARKOPS_SESSION_SECONDS",
            28800,
        )

    if lifetime <= 0:
        raise AuthenticationError("Invalid session lifetime.")

    expires_at = _utcnow() + timedelta(seconds=lifetime)

    return create_session(
        user=user,
        expires_at=expires_at,
        remember_device=remember_device,
        revoke_existing_sessions=True,
    )


def get_session_cookie_name():
    return current_app.config.get(
        "DARKOPS_SESSION_COOKIE",
        "darkops_session",
    )


def get_session_token():
    return request.cookies.get(get_session_cookie_name())


def authenticate_session(raw_session_token=None, touch=True):
    raw_session_token = raw_session_token or get_session_token()

    if not raw_session_token:
        return None

    token_hash = _hash_token(raw_session_token)

    session = Session.query.filter_by(
        session_token_hash=token_hash,
        status="active",
    ).first()

    if not session:
        return None

    now = _utcnow()

    if session.expires_at <= now:
        session.status = "expired"
        db.session.commit()
        return None

    user = _validate_user(session.user)

    if not user:
        session.status = "revoked"
        session.revoked_at = now
        db.session.commit()
        return None

    if touch:
        touch_session(session)

    g.current_user = user
    g.current_session = session

    return user


def restore_remembered_session(turnstile_token, raw_session_token=None):
    verify_session_resume_challenge(turnstile_token)

    return authenticate_session(
        raw_session_token=raw_session_token,
        touch=True,
    )


def set_session_cookie(response, raw_session_token, session, remember_device=False):
    cookie_name = get_session_cookie_name()
    secure = current_app.config.get("DARKOPS_COOKIE_SECURE", True)
    samesite = current_app.config.get("DARKOPS_COOKIE_SAMESITE", "Lax")

    kwargs = {
        "httponly": True,
        "secure": secure,
        "samesite": samesite,
        "path": "/",
    }

    if remember_device:
        remaining = int(
            (session.expires_at - _utcnow()).total_seconds()
        )
        kwargs["max_age"] = max(remaining, 0)

    response.set_cookie(
        cookie_name,
        raw_session_token,
        **kwargs,
    )

    return response


def clear_session_cookie(response):
    response.delete_cookie(
        get_session_cookie_name(),
        path="/",
    )

    return response


def get_current_user():
    return getattr(g, "current_user", None)


def get_current_session():
    return getattr(g, "current_session", None)


def is_authenticated():
    return get_current_user() is not None


def touch_session(session=None):
    session = session or get_current_session()

    if not session:
        return None

    if session.status != "active":
        return session

    now = _utcnow()

    if session.expires_at <= now:
        session.status = "expired"
        db.session.commit()
        return session

    interval = current_app.config.get(
        "DARKOPS_PRESENCE_UPDATE_SECONDS",
        60,
    )

    if (
        session.last_seen_at is None
        or (now - session.last_seen_at).total_seconds() >= interval
    ):
        session.last_seen_at = now
        db.session.commit()

    return session


def get_presence(user=None):
    user = user or get_current_user()

    if not user:
        return {
            "authenticated": False,
            "present": False,
            "last_seen_at": None,
        }

    session = get_current_session()

    if not session:
        session = Session.query.filter_by(
            user_id=user.id,
            status="active",
        ).order_by(
            Session.last_seen_at.desc()
        ).first()

    if not session:
        return {
            "authenticated": True,
            "present": False,
            "last_seen_at": None,
        }

    return {
        "authenticated": True,
        "present": session_is_active(session),
        "last_seen_at": session.last_seen_at,
    }


def is_recently_active(user, days=7):
    if not user or days <= 0:
        return False

    cutoff = _utcnow() - timedelta(days=days)

    last_activity = Session.query.filter(
        Session.user_id == user.id,
        Session.last_seen_at.isnot(None),
    ).order_by(
        Session.last_seen_at.desc()
    ).first()

    if not last_activity or not last_activity.last_seen_at:
        return False

    return last_activity.last_seen_at >= cutoff


def revoke_session(session=None):
    session = session or get_current_session()

    if not session:
        return False

    if session.status != "active":
        return False

    session.status = "revoked"
    session.revoked_at = _utcnow()

    db.session.commit()

    if getattr(g, "current_session", None) is session:
        g.current_session = None
        g.current_user = None

    return True


def revoke_other_sessions(user, current_session_id=None):
    if not user:
        return 0

    query = Session.query.filter(
        Session.user_id == user.id,
        Session.status == "active",
    )

    if current_session_id:
        query = query.filter(
            Session.id != current_session_id,
        )

    sessions = query.all()

    if not sessions:
        return 0

    now = _utcnow()

    for session in sessions:
        session.status = "revoked"
        session.revoked_at = now

    db.session.commit()

    return len(sessions)


def revoke_all_sessions(user):
    return revoke_other_sessions(user)


def expire_stale_sessions():
    now = _utcnow()

    count = Session.query.filter(
        Session.status == "active",
        Session.expires_at <= now,
    ).update(
        {
            "status": "expired",
        },
        synchronize_session=False,
    )

    db.session.commit()

    return count


def session_is_active(session):
    if not session:
        return False

    if session.status != "active":
        return False

    if session.expires_at <= _utcnow():
        return False

    return True


def user_has_active_session(user):
    if not user:
        return False

    session = Session.query.filter_by(
        user_id=user.id,
        status="active",
    ).order_by(
        Session.last_seen_at.desc()
    ).first()

    if not session:
        return False

    if session.expires_at <= _utcnow():
        session.status = "expired"
        db.session.commit()
        return False

    return True
