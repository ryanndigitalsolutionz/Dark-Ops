import uuid
from datetime import datetime, timezone
from extensions import db


class TeamInvitation(db.Model):
    __tablename__ = "team_invitation"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), nullable=False, index=True)
    role_id = db.Column(db.String(36), db.ForeignKey("team_role.id"), nullable=False, index=True)
    invited_by_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    accepted_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=True, index=True)
    email = db.Column(db.String(320), nullable=False)
    token_hash = db.Column(db.Text, unique=True, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="pending", index=True)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    invited_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    accepted_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    team = db.relationship("Team", back_populates="invitations")
    role = db.relationship("TeamRole", back_populates="invitations")
    invited_by = db.relationship("User", foreign_keys=[invited_by_user_id], back_populates="sent_team_invitations")
    accepted_user = db.relationship("User", foreign_keys=[accepted_user_id], back_populates="accepted_team_invitations")
