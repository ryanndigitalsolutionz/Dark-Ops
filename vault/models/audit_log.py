import uuid
from datetime import datetime, timezone
from extensions import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), index=True)
    actor_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), index=True)
    application_id = db.Column(db.String(36), db.ForeignKey("application.id"), index=True)
    api_key_id = db.Column(db.String(36), db.ForeignKey("api_key.id"), index=True)
    subscription_id = db.Column(db.String(36), db.ForeignKey("subscription.id"), index=True)
    asset_id = db.Column(db.String(36), db.ForeignKey("asset.id"), index=True)
    event_id = db.Column(db.String(36), db.ForeignKey("event.id"), index=True)
    alert_id = db.Column(db.String(36), db.ForeignKey("alert.id"), index=True)
    incident_id = db.Column(db.String(36), db.ForeignKey("incident.id"), index=True)
    access_method = db.Column(db.String(20), nullable=False, index=True)
    action = db.Column(db.String(150), nullable=False, index=True)
    resource_type = db.Column(db.String(100), nullable=False)
    resource_id = db.Column(db.String(36), index=True)
    ip_address = db.Column(db.String(255))
    user_agent = db.Column(db.String(1000))
    metadata_ = db.Column("metadata", db.JSON)
    occurred_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    team = db.relationship("Team", back_populates="audit_logs")
    actor_user = db.relationship("User", back_populates="audit_logs")
    application = db.relationship("Application", back_populates="audit_logs")
    api_key = db.relationship("ApiKey", back_populates="audit_logs")
    subscription = db.relationship("Subscription", back_populates="audit_logs")
    asset = db.relationship("Asset", back_populates="audit_logs")
    event = db.relationship("Event", back_populates="audit_logs")
    alert = db.relationship("Alert", back_populates="audit_logs")
    incident = db.relationship("Incident", back_populates="audit_logs")
    incident_notes = db.relationship("IncidentNote", back_populates="audit_log")
