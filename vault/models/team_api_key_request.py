import uuid
from datetime import datetime, timezone
from extensions import db


class TeamApiKeyRequest(db.Model):
    __tablename__ = "team_api_key_request"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = db.Column(db.String(30), unique=True, nullable=False, index=True)
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), nullable=False, index=True)
    application_id = db.Column(db.String(36), db.ForeignKey("application.id"), nullable=False, index=True)
    subscription_id = db.Column(db.String(36), db.ForeignKey("subscription.id"), nullable=False, index=True)
    requested_by_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    reviewed_by_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=True, index=True)
    name = db.Column(db.String(150), nullable=False)
    mode = db.Column(db.String(20), nullable=False, index=True)
    environment = db.Column(db.String(20), nullable=False, default="test", index=True)
    reason = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), nullable=False, default="pending", index=True)
    vote_threshold = db.Column(db.Numeric(5, 2), nullable=False, default=60)
    total_vote_percentage = db.Column(db.Numeric(7, 2), nullable=False, default=0)
    vote_count = db.Column(db.Integer, nullable=False, default=0)
    owner_decision = db.Column(db.String(20), nullable=True)
    owner_decided_at = db.Column(db.DateTime(timezone=True), nullable=True)
    api_key_id = db.Column(db.String(36), db.ForeignKey("api_key.id"), nullable=True, unique=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime(timezone=True), nullable=True)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    team = db.relationship("Team", backref="team_api_key_requests")
    application = db.relationship("Application", backref="team_api_key_requests")
    subscription = db.relationship("Subscription", backref="team_api_key_requests")
    requested_by_user = db.relationship("User", foreign_keys=[requested_by_user_id], backref="team_api_key_requests")
    reviewed_by_user = db.relationship("User", foreign_keys=[reviewed_by_user_id], backref="reviewed_team_api_key_requests")
    resulting_api_key = db.relationship("ApiKey", foreign_keys=[api_key_id], back_populates="team_api_key_request", uselist=False)
    votes = db.relationship("TeamApiKeyVote", back_populates="request", cascade="all, delete-orphan")
