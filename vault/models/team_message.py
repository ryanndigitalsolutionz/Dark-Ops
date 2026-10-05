import uuid
from datetime import datetime, timezone
from extensions import db


class TeamMessage(db.Model):
    __tablename__ = "team_message"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), nullable=False, index=True)
    sender_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    reply_to_message_id = db.Column(db.String(36), db.ForeignKey("team_message.id"), nullable=True, index=True)
    content = db.Column(db.Text, nullable=False)
    is_edited = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    edited_at = db.Column(db.DateTime(timezone=True))
    deleted_at = db.Column(db.DateTime(timezone=True))

    team = db.relationship("Team", back_populates="messages")
    sender = db.relationship("User", back_populates="sent_team_messages")
    reply_to = db.relationship("TeamMessage", remote_side=[id], backref="replies")
