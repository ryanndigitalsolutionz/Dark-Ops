import uuid
from datetime import datetime, timezone
from extensions import db


class RecoveryCode(db.Model):
    __tablename__ = "recovery_code"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    code_hash = db.Column(db.Text, unique=True, nullable=False, index=True)
    used_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    user = db.relationship(
        "User",
        back_populates="recovery_codes"
    )
