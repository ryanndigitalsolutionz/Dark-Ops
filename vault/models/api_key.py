import uuid
from datetime import datetime, timezone
from extensions import db


class ApiKey(db.Model):
    __tablename__ = "api_key"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), nullable=True, index=True)
    application_id = db.Column(db.String(36), db.ForeignKey("application.id"), nullable=False, index=True)
    subscription_id = db.Column(db.String(36), db.ForeignKey("subscription.id"), nullable=False, index=True)
    created_by_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    mode = db.Column(db.String(20), nullable=False, index=True)
    environment = db.Column(db.String(20), nullable=False, default="test", index=True)
    public_key = db.Column(db.String(255), nullable=False, unique=True, index=True)
    secret_key_hash = db.Column(db.String(255), nullable=False)
    secret_key_prefix = db.Column(db.String(32), nullable=False)
    public_scopes = db.Column(db.JSON)
    secret_scopes = db.Column(db.JSON)
    status = db.Column(db.String(30), nullable=False, default="active", index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime(timezone=True))
    last_used_at = db.Column(db.DateTime(timezone=True))
    rotated_at = db.Column(db.DateTime(timezone=True))
    revoked_at = db.Column(db.DateTime(timezone=True))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner_user = db.relationship("User", foreign_keys=[owner_user_id], back_populates="owned_api_keys")
    team = db.relationship("Team", back_populates="api_keys")
    application = db.relationship("Application", back_populates="api_keys")
    subscription = db.relationship("Subscription", back_populates="api_keys")
    created_by_user = db.relationship("User", foreign_keys=[created_by_user_id], back_populates="created_api_keys")
    usage_meters = db.relationship("UsageMeter", back_populates="api_key")
    audit_logs = db.relationship("AuditLog", back_populates="api_key")
    team_api_key_request = db.relationship("TeamApiKeyRequest", back_populates="resulting_api_key", uselist=False)
