import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from flask import current_app

from extensions import db
from models.alert import Alert
from models.application import Application
from models.incident import Incident
from models.recovery_operation import RecoveryOperation
from models.user import User
from models.vulnerability import Vulnerability


SEVERITY_PENALTY = {
    "informational": 0,
    "low": 5,
    "medium": 15,
    "high": 30,
    "critical": 50,
}

POSTURE_WEIGHTS = {
    "detection": 30,
    "alerts": 20,
    "incidents": 20,
    "vulnerabilities": 15,
    "recovery": 10,
    "availability": 5,
}


class PostureError(Exception):
    pass


def utcnow():
    return datetime.now(timezone.utc)


def _clamp(score):
    return max(0, min(100, round(score)))


def _severity_penalty(severity):
    return SEVERITY_PENALTY.get(
        str(severity).lower(),
        0,
    )


def _detection_state(application):
    state = getattr(application, "detection_state", None)

    if not isinstance(state, dict):
        return {}

    checks = state.get("checks")

    return checks if isinstance(checks, dict) else {}


def _score_detection(application):
    checks = _detection_state(application)

    if not checks:
        return 100

    score = 100

    for check in checks.values():
        if not isinstance(check, dict):
            continue

        if not check.get("security_relevant"):
            continue

        score -= _severity_penalty(
            check.get("severity")
        )

    return _clamp(score)


def _score_alerts(application):
    alerts = Alert.query.filter(
        Alert.application_id == application.id,
        Alert.status.in_([
            "open",
            "acknowledged",
            "investigating",
        ]),
    ).all()

    score = 100

    for alert in alerts:
        score -= _severity_penalty(
            alert.severity
        )

    return _clamp(score)


def _score_incidents(application):
    incidents = Incident.query.filter(
        Incident.application_id == application.id,
        Incident.status.in_([
            "open",
            "investigating",
            "contained",
        ]),
    ).all()

    score = 100

    for incident in incidents:
        score -= _severity_penalty(
            incident.severity
        )

    return _clamp(score)


def _score_vulnerabilities(application):
    count = Vulnerability.query.filter(
        Vulnerability.application_id == application.id,
        Vulnerability.status.in_([
            "open",
            "acknowledged",
            "resolving",
        ]),
    ).count()

    return _clamp(
        100 - (count * 15)
    )


def _score_recovery(application):
    operations = RecoveryOperation.query.filter_by(
        application_id=application.id,
    ).all()

    unresolved = 0

    for operation in operations:
        if operation.verification_status != "verified":
            unresolved += 1

    return _clamp(
        100 - (unresolved * 20)
    )


def _score_availability(application):
    return 100 if application.status == "connected" else 0


def _weighted_score(components):
    numerator = 0
    denominator = 0

    for key, weight in POSTURE_WEIGHTS.items():
        score = components.get(key)

        if score is None:
            continue

        numerator += score * weight
        denominator += weight

    if denominator == 0:
        return None

    return _clamp(
        numerator / denominator
    )


def get_application_posture(application):
    if not application:
        raise PostureError("Application is required.")

    components = {
        "detection": _score_detection(application),
        "alerts": _score_alerts(application),
        "incidents": _score_incidents(application),
        "vulnerabilities": _score_vulnerabilities(application),
        "recovery": _score_recovery(application),
        "availability": _score_availability(application),
    }

    score = _weighted_score(components)

    return {
        "application_id": application.id,
        "score": score,
        "status": (
            "healthy" if score is not None and score >= 80
            else "attention" if score is not None and score >= 60
            else "at_risk" if score is not None
            else "unknown"
        ),
        "components": components,
        "detection": {
            "last_cycle_at": (
                getattr(application, "detection_state", {})
                or {}
            ).get("last_cycle_at"),
            "checks": len(
                _detection_state(application)
            ),
        },
        "generated_at": utcnow(),
    }


def _request_hibp(email):
    api_key = current_app.config.get(
        "HIBP_API_KEY"
    )

    if not api_key:
        return {
            "status": "unavailable",
            "breached": None,
            "breach_count": None,
        }

    encoded_email = urllib.parse.quote(
        email,
        safe="",
    )

    url = (
        "https://haveibeenpwned.com/api/v3/"
        f"breachedaccount/{encoded_email}"
        "?truncateResponse=false"
    )

    request = urllib.request.Request(
        url,
        headers={
            "hibp-api-key": api_key,
            "user-agent": current_app.config.get(
                "HIBP_USER_AGENT",
                "DarkOps/1.0",
            ),
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=10,
        ) as response:
            payload = json.loads(
                response.read().decode("utf-8")
            )

            return {
                "status": "breached",
                "breached": True,
                "breach_count": len(payload),
            }

    except urllib.error.HTTPError as error:
        if error.code == 404:
            return {
                "status": "clear",
                "breached": False,
                "breach_count": 0,
            }

        if error.code == 429:
            return {
                "status": "rate_limited",
                "breached": None,
                "breach_count": None,
            }

        return {
            "status": "unavailable",
            "breached": None,
            "breach_count": None,
        }

    except (urllib.error.URLError, ValueError, json.JSONDecodeError):
        return {
            "status": "unavailable",
            "breached": None,
            "breach_count": None,
        }


def get_user_posture(user):
    if not user:
        raise PostureError("User is required.")

    hibp = _request_hibp(user.email)

    if hibp["status"] == "clear":
        score = 100

    elif hibp["status"] == "breached":
        score = _clamp(
            100 - (hibp["breach_count"] * 20)
        )

    else:
        score = None

    return {
        "user_id": user.id,
        "darkops_id": user.darkops_id,
        "health_score": score,
        "status": (
            "healthy" if score is not None and score >= 80
            else "attention" if score is not None and score >= 60
            else "at_risk" if score is not None
            else "unknown"
        ),
        "breach_exposure": {
            "status": hibp["status"],
            "breached": hibp["breached"],
            "breach_count": hibp["breach_count"],
        },
        "generated_at": utcnow(),
    }


def get_team_user_postures(users):
    return [
        get_user_posture(user)
        for user in users or []
        if isinstance(user, User)
    ]
