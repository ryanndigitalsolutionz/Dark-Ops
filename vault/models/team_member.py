import uuid
from datetime import datetime, timezone
from extensions import db


class TeamMember(db.Model):
    __tablename__ = "team_member"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    role_id = db.Column(db.String(36), db.ForeignKey("team_role.id"), nullable=False, index=True)
    status = db.Column(db.String(30), nullable=False, default="active", index=True)
    team_access_enabled = db.Column(db.Boolean, nullable=False, default=True, index=True)
    team_access_disabled_until = db.Column(db.DateTime(timezone=True), nullable=True, index=True)
    access_schedule = db.Column(db.JSON, nullable=True)
    joined_at = db.Column(db.DateTime(timezone=True))
    suspended_at = db.Column(db.DateTime(timezone=True))
    left_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    team = db.relationship("Team", back_populates="members")
    user = db.relationship("User", back_populates="team_memberships")
    role = db.relationship("TeamRole", back_populates="members")

    __table_args__ = (
        db.UniqueConstraint("team_id", "user_id", name="uq_team_member_user"),
    )