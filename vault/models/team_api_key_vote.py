import uuid
from datetime import datetime, timezone
from extensions import db


class TeamApiKeyVote(db.Model):
    __tablename__ = "team_api_key_vote"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = db.Column(db.String(36), db.ForeignKey("team_api_key_request.id"), nullable=False, index=True)
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), nullable=False, index=True)
    voter_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    vote_percentage = db.Column(db.Numeric(5, 2), nullable=False)
    decision = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    request = db.relationship("TeamApiKeyRequest", back_populates="votes")
    team = db.relationship("Team", backref="team_api_key_votes")
    voter_user = db.relationship("User", backref="team_api_key_votes")

    __table_args__ = (
        db.UniqueConstraint("request_id", "voter_user_id", name="uq_team_api_key_vote"),
        db.CheckConstraint("vote_percentage >= 0 AND vote_percentage <= 100", name="ck_team_api_key_vote_percentage"),
    )
