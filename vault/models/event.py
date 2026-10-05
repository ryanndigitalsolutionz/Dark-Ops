import uuid
from datetime import datetime, timezone
from extensions import db


class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    application_id = db.Column(
        db.String(36),
        db.ForeignKey("application.id"),
        nullable=False,
        index=True,
    )

    asset_id = db.Column(
        db.String(36),
        db.ForeignKey("asset.id"),
        nullable=True,
        index=True,
    )

    source = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=True, index=True)
    event_type = db.Column(db.String(150), nullable=False, index=True)
    detection_check = db.Column(db.String(150), nullable=True, index=True)

    verification_mode = db.Column(
        db.String(50),
        nullable=False,
        default="passive",
        index=True,
    )

    origin = db.Column(
        db.String(50),
        nullable=False,
        default="darkops",
        index=True,
    )

    severity = db.Column(db.String(20), nullable=False, index=True)
    confidence = db.Column(db.Numeric(5, 4), nullable=True)

    fingerprint = db.Column(db.String(255), nullable=True, index=True)

    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    actor_identifier = db.Column(db.String(255), nullable=True)

    payload = db.Column(db.JSON, nullable=True)

    occurred_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    received_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        db.Index(
            "ix_event_application_fingerprint",
            "application_id",
            "fingerprint",
        ),
    )

    application = db.relationship(
        "Application",
        back_populates="events",
    )

    asset = db.relationship(
        "Asset",
        back_populates="events",
    )

    alerts = db.relationship(
        "Alert",
        back_populates="event",
    )

    notifications = db.relationship(
        "Notification",
        back_populates="event",
    )

    usage_meters = db.relationship(
        "UsageMeter",
        back_populates="event",
    )

    audit_logs = db.relationship(
        "AuditLog",
        back_populates="event",
    )
