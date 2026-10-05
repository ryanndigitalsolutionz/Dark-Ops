import uuid
from datetime import datetime, timezone
from extensions import db


class ResponseConnector(db.Model):
    __tablename__ = "response_connector"

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

    type = db.Column(
        db.String(100),
        nullable=False,
        index=True,
    )

    base_url = db.Column(db.Text)

    configuration_encrypted = db.Column(db.Text)

    status = db.Column(
        db.String(30),
        nullable=False,
        default="inactive",
        index=True,
    )

    metadata_ = db.Column("metadata", db.JSON)

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
        back_populates="response_connectors",
    )

    created_by_user = db.relationship(
        "User",
        back_populates="created_response_connectors",
    )

    response_decisions = db.relationship(
        "ResponseDecision",
        back_populates="response_connector",
    )
