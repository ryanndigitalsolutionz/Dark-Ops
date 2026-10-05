import uuid
from datetime import datetime, timezone
from extensions import db


class Session(db.Model):
    __tablename__ = "session"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    session_token_hash = db.Column(db.Text, unique=True, nullable=False, index=True)
    refresh_token_hash = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="active", index=True)
    ip_address = db.Column(db.String(255), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    last_seen_at = db.Column(db.DateTime(timezone=True), nullable=True)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime(timezone=True), nullable=True)

    user = db.relationship(
        "User",
        back_populates="sessions"
    )
