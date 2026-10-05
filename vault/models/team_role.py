import uuid
from datetime import datetime, timezone
from extensions import db


class TeamRole(db.Model):
    __tablename__ = "team_role"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_system_role = db.Column(db.Boolean, nullable=False, default=False)
    permissions = db.Column(db.JSON, nullable=False, default=dict)
    console_layout = db.Column(db.JSON)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    team = db.relationship("Team", back_populates="roles")
    members = db.relationship("TeamMember", back_populates="role")
    invitations = db.relationship("TeamInvitation", back_populates="role")

    __table_args__ = (
        db.UniqueConstraint("team_id", "name", name="uq_team_role_name"),
    )
