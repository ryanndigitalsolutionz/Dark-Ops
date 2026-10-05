import uuid
from datetime import datetime, timezone
from extensions import db


class Incident(db.Model):
    __tablename__ = "incident"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    application_id = db.Column(
        db.String(36),
        db.ForeignKey("application.id"),
        nullable=False,
        index=True,
    )

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    severity = db.Column(
        db.String(20),
        nullable=False,
        index=True,
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="open",
        index=True,
    )

    assigned_to_user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.id"),
        nullable=True,
        index=True,
    )

    opened_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    contained_at = db.Column(db.DateTime(timezone=True))
    resolved_at = db.Column(db.DateTime(timezone=True))
    closed_at = db.Column(db.DateTime(timezone=True))

    resolution = db.Column(db.Text)
    metadata_ = db.Column("metadata", db.JSON)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    application = db.relationship(
        "Application",
        back_populates="incidents",
    )

    assigned_to = db.relationship(
        "User",
        foreign_keys=[assigned_to_user_id],
        backref="assigned_incidents",
    )

    alerts = db.relationship(
        "Alert",
        back_populates="incident",
    )

    notes = db.relationship(
        "IncidentNote",
        back_populates="incident",
        cascade="all, delete-orphan",
    )

    actions = db.relationship(
        "IncidentAction",
        back_populates="incident",
        cascade="all, delete-orphan",
    )

    response_decisions = db.relationship(
        "ResponseDecision",
        back_populates="incident",
        cascade="all, delete-orphan",
    )

    recovery_operations = db.relationship(
        "RecoveryOperation",
        back_populates="incident",
    )

    notifications = db.relationship(
        "Notification",
        back_populates="incident",
    )

    audit_logs = db.relationship(
        "AuditLog",
        back_populates="incident",
    )
