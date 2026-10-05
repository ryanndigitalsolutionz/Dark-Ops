import uuid
from datetime import datetime, timezone
from extensions import db


class TeamNotificationRule(db.Model):
    __tablename__ = "team_notification_rule"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), nullable=False, index=True)
    application_id = db.Column(db.String(36), db.ForeignKey("application.id"), nullable=True, index=True)
    created_by_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    target_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    minimum_severity = db.Column(db.String(30), nullable=True, index=True)
    event_types = db.Column(db.JSON)
    notification_channels = db.Column(db.JSON)
    enabled = db.Column(db.Boolean, nullable=False, default=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    team = db.relationship("Team", back_populates="notification_rules")
    application = db.relationship("Application", back_populates="notification_rules")
    created_by_user = db.relationship("User", foreign_keys=[created_by_user_id], back_populates="created_notification_rules")
    target_user = db.relationship("User", foreign_keys=[target_user_id], back_populates="notification_targets")
