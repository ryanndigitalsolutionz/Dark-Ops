from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc)


def ensure_utc(value):
    if value is None:
        return None

    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)
