import uuid
from datetime import datetime, timezone
from extensions import db


class MfaFactor(db.Model):
    __tablename__ = "mfa_factor"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    type = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    secret_encrypted = db.Column(db.Text, nullable=False)
    is_primary = db.Column(db.Boolean, nullable=False, default=True)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    verified_at = db.Column(db.DateTime(timezone=True), nullable=True)
    last_used_at = db.Column(db.DateTime(timezone=True), nullable=True)

    user = db.relationship(
        "User",
        back_populates="mfa_factors"
    )
