import uuid
from datetime import datetime, timezone
from extensions import db


class RecoveryOperation(db.Model):
    __tablename__ = "recovery_operation"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    incident_id = db.Column(
        db.String(36),
        db.ForeignKey("incident.id"),
        nullable=False,
        index=True,
    )

    initiated_by_user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.id"),
        nullable=True,
        index=True,
    )

    actor_type = db.Column(
        db.String(20),
        nullable=False,
        default="user",
        index=True,
    )

    operation_type = db.Column(
        db.String(150),
        nullable=False,
        index=True,
    )

    target = db.Column(db.Text)

    status = db.Column(
        db.String(30),
        nullable=False,
        default="pending",
        index=True,
    )

    parameters = db.Column(db.JSON)
    result = db.Column(db.JSON)
    verification_metadata = db.Column(db.JSON)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    started_at = db.Column(
        db.DateTime(timezone=True),
    )

    completed_at = db.Column(
        db.DateTime(timezone=True),
    )

    verified_at = db.Column(
        db.DateTime(timezone=True),
    )

    incident = db.relationship(
        "Incident",
        back_populates="recovery_operations",
    )

    initiated_by_user = db.relationship(
        "User",
        back_populates="initiated_recovery_operations",
    )
