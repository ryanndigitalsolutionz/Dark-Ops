import uuid
from datetime import datetime, timezone
from extensions import db


class ResponsePolicy(db.Model):
    __tablename__ = "response_policy"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    team_id = db.Column(
        db.String(36),
        db.ForeignKey("team.id"),
        nullable=False,
        index=True,
    )

    created_by_user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.id"),
        nullable=False,
        index=True,
    )

    name = db.Column(
        db.String(150),
        nullable=False,
    )

    description = db.Column(db.Text)

    execution_mode = db.Column(
        db.String(30),
        nullable=False,
        default="approval_required",
        index=True,
    )

    triggers = db.Column(db.JSON)
    rules = db.Column(db.JSON)

    enabled = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        index=True,
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

    team = db.relationship(
        "Team",
        back_populates="response_policies",
    )

    created_by_user = db.relationship(
        "User",
        back_populates="created_response_policies",
    )

    response_decisions = db.relationship(
        "ResponseDecision",
        back_populates="response_policy",
    )
