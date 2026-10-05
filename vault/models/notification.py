import uuid
from datetime import datetime, timezone

from extensions import db


class Notification(db.Model):
    __tablename__ = "notification"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.id"),
        nullable=False,
        index=True,
    )

    team_id = db.Column(
        db.String(36),
        db.ForeignKey("team.id"),
        nullable=True,
        index=True,
    )

    sender_user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.id"),
        nullable=True,
        index=True,
    )

    event_id = db.Column(
        db.String(36),
        db.ForeignKey("event.id"),
        nullable=True,
        index=True,
    )

    alert_id = db.Column(
        db.String(36),
        db.ForeignKey("alert.id"),
        nullable=True,
        index=True,
    )

    incident_id = db.Column(
        db.String(36),
        db.ForeignKey("incident.id"),
        nullable=True,
        index=True,
    )

    vulnerability_id = db.Column(
        db.String(36),
        db.ForeignKey("vulnerability.id"),
        nullable=True,
        index=True,
    )

    type = db.Column(
        db.String(40),
        nullable=False,
        index=True,
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="unread",
        index=True,
    )

    title = db.Column(
        db.String(255),
        nullable=False,
    )

    message = db.Column(
        db.Text,
        nullable=False,
    )

    sound_key = db.Column(
        db.String(100),
        nullable=True,
    )

    action_key = db.Column(
        db.String(100),
        nullable=True,
    )

    action_url = db.Column(
        db.Text,
        nullable=True,
    )

    metadata_ = db.Column("metadata", db.JSON, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    read_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    user = db.relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="notifications",
    )

    team = db.relationship(
        "Team",
        back_populates="notifications",
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_user_id],
        back_populates="sent_notifications",
    )

    event = db.relationship(
        "Event",
        back_populates="notifications",
    )

    alert = db.relationship(
        "Alert",
        back_populates="notifications",
    )

    incident = db.relationship(
        "Incident",
        back_populates="notifications",
    )

    vulnerability = db.relationship(
        "Vulnerability",
        back_populates="notifications",
    )
