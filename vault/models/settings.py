import uuid
from datetime import datetime, timezone
from extensions import db


class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, unique=True, index=True)
    profile_id = db.Column(db.String(36), db.ForeignKey("profile.id"), nullable=False, unique=True, index=True)
    theme = db.Column(db.String(20), nullable=False, default="dark")
    timezone = db.Column(db.String(100), nullable=True)
    default_environment = db.Column(db.String(20), nullable=False, default="test")
    email_notifications = db.Column(db.Boolean, nullable=False, default=True)
    security_notifications = db.Column(db.Boolean, nullable=False, default=True)
    announcement_notifications = db.Column(db.Boolean, nullable=False, default=True)
    privacy_preferences = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship(
        "User",
        back_populates="settings"
    )

    profile = db.relationship(
        "Profile",
        back_populates="settings"
    )
