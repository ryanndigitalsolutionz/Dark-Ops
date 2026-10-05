import uuid
from datetime import datetime, timezone
from extensions import db


class Profile(db.Model):
    __tablename__ = "profile"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    first_name = db.Column(
        db.String(100),
        nullable=True,
    )

    surname = db.Column(
        db.String(100),
        nullable=True,
    )

    last_name = db.Column(
        db.String(100),
        nullable=True,
    )

    display_name = db.Column(
        db.String(150),
        nullable=True,
    )

    avatar_url = db.Column(
        db.Text,
        nullable=True,
    )

    bio = db.Column(
        db.Text,
        nullable=True,
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

    user = db.relationship(
        "User",
        back_populates="profile",
    )

    completion = db.relationship(
        "ProfileCompletion",
        back_populates="profile",
        uselist=False,
        cascade="all, delete-orphan",
    )
