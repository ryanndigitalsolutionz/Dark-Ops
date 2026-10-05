import uuid
from datetime import datetime, timezone
from extensions import db


class IncidentNote(db.Model):
    __tablename__ = "incident_note"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = db.Column(db.String(36), db.ForeignKey("incident.id"), nullable=False, index=True)
    author_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)

    audit_log_id = db.Column(
        db.String(36),
        db.ForeignKey("audit_logs.id"),
        nullable=True,
        index=True,
    )

    actor_type = db.Column(db.String(20), nullable=False, default="user", index=True)
    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = db.Column(db.DateTime(timezone=True))

    incident = db.relationship("Incident", back_populates="notes")
    author = db.relationship("User", back_populates="incident_notes")
    audit_log = db.relationship("AuditLog", back_populates="incident_notes")
