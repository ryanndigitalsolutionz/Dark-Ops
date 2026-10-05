import uuid
from datetime import datetime, timezone
from extensions import db


class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    owner_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=True, index=True)
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), nullable=True, index=True)
    created_by_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)

    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    environment = db.Column(db.String(20), nullable=False, default="test", index=True)
    status = db.Column(db.String(30), nullable=False, default="disconnected", index=True)

    authorized_primary_url = db.Column(db.Text, nullable=False)
    base_url = db.Column(db.Text)
    description = db.Column(db.Text)

    detection_state = db.Column(db.JSON, nullable=False, default=dict)

    webhook_url = db.Column(db.Text)
    webhook_secret_hash = db.Column(db.Text)
    webhook_secret_prefix = db.Column(db.String(32))
    webhook_active = db.Column(db.Boolean, nullable=False, default=False)
    webhook_events = db.Column(db.JSON)
    webhook_last_delivery_at = db.Column(db.DateTime(timezone=True))

    connected_at = db.Column(db.DateTime(timezone=True))
    disconnected_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner = db.relationship("User", foreign_keys=[owner_user_id], back_populates="owned_applications")
    team = db.relationship("Team", back_populates="applications")
    created_by = db.relationship("User", foreign_keys=[created_by_user_id], back_populates="created_applications")
    assets = db.relationship("Asset", back_populates="application")
    alerts = db.relationship("Alert", back_populates="application")
    events = db.relationship("Event", back_populates="application")
    incidents = db.relationship("Incident", back_populates="application")
    vulnerabilities = db.relationship("Vulnerability", back_populates="application")
    audit_logs = db.relationship("AuditLog", back_populates="application")

    __table_args__ = (
        db.UniqueConstraint(
            "owner_user_id",
            "slug",
            "environment",
            name="uq_application_owner_slug_environment",
        ),
        db.UniqueConstraint(
            "team_id",
            "slug",
            "environment",
            name="uq_application_team_slug_environment",
        ),
        db.CheckConstraint(
            "(owner_user_id IS NOT NULL AND team_id IS NULL) "
            "OR (owner_user_id IS NULL AND team_id IS NOT NULL)",
            name="ck_application_owner_or_team",
        ),
    )
