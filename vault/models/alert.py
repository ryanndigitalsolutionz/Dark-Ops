import uuid
from datetime import datetime, timezone
from extensions import db


class Alert(db.Model):
    __tablename__ = "alert"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    application_id = db.Column(db.String(36), db.ForeignKey("application.id"), nullable=False, index=True)
    asset_id = db.Column(db.String(36), db.ForeignKey("asset.id"), index=True)
    event_id = db.Column(db.String(36), db.ForeignKey("event.id"), index=True)
    incident_id = db.Column(db.String(36), db.ForeignKey("incident.id"), index=True)

    created_by_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), index=True)
    origin = db.Column(db.String(30), nullable=False, default="darkops", index=True)

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    alert_type = db.Column(db.String(150), nullable=False, index=True)
    severity = db.Column(db.String(20), nullable=False, index=True)
    status = db.Column(db.String(30), nullable=False, default="open", index=True)
    assigned_to_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), index=True)

    first_seen_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    last_seen_at = db.Column(db.DateTime(timezone=True))
    acknowledged_at = db.Column(db.DateTime(timezone=True))
    resolved_at = db.Column(db.DateTime(timezone=True))

    metadata_ = db.Column("metadata", db.JSON)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    application = db.relationship("Application", back_populates="alerts")
    asset = db.relationship("Asset", back_populates="alerts")
    event = db.relationship("Event", back_populates="alerts")
    incident = db.relationship("Incident", back_populates="alerts")
    created_by = db.relationship("User", foreign_keys=[created_by_user_id], backref="created_alerts")
    assigned_to = db.relationship("User", foreign_keys=[assigned_to_user_id], backref="assigned_alerts")
    notifications = db.relationship("Notification", back_populates="alert")
    audit_logs = db.relationship("AuditLog", back_populates="alert")
