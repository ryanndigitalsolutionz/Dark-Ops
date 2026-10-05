import uuid
from datetime import datetime, timezone
from extensions import db


class TeamOwner(db.Model):
    __tablename__ = "team_owner"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    assigned_by_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    status = db.Column(db.String(30), nullable=False, default="active", index=True)
    assigned_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    removed_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    team = db.relationship("Team", back_populates="team_owners")
    user = db.relationship("User", foreign_keys=[user_id], back_populates="team_ownerships")
    assigned_by_user = db.relationship("User", foreign_keys=[assigned_by_user_id], back_populates="assigned_team_owners")

    __table_args__ = (
        db.UniqueConstraint("team_id", "user_id", name="uq_team_owner"),
    )
