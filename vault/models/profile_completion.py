import uuid
from datetime import datetime, timezone
from extensions import db


class ProfileCompletion(db.Model):
    __tablename__ = "profile_completion"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    profile_id = db.Column(
        db.String(36),
        db.ForeignKey("profile.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    phone_verified = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    identity_completed = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    presentation_completed = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    payment_verified = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    completion_percentage = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    initial_completion_reward_granted = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    profile = db.relationship(
        "Profile",
        back_populates="completion",
    )
