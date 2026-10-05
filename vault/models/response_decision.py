import uuid
from datetime import datetime, timezone
from extensions import db


class ResponseDecision(db.Model):
    __tablename__ = "response_decision"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    incident_id = db.Column(
        db.String(36),
        db.ForeignKey("incident.id"),
        nullable=False,
        index=True,
    )

    policy_id = db.Column(
        db.String(36),
        db.ForeignKey("response_policy.id"),
        nullable=True,
        index=True,
    )

    connector_id = db.Column(
        db.String(36),
        db.ForeignKey("response_connector.id"),
        nullable=True,
        index=True,
    )

    action_type = db.Column(
        db.String(150),
        nullable=False,
    )

    execution_mode = db.Column(
        db.String(30),
        nullable=False,
        index=True,
    )

    target_scope = db.Column(
        db.String(50),
        nullable=False,
    )

    target = db.Column(db.Text)

    status = db.Column(
        db.String(30),
        nullable=False,
        default="pending",
        index=True,
    )

    rationale = db.Column(db.Text)

    decided_by_user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.id"),
        nullable=True,
        index=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )

    approved_at = db.Column(
        db.DateTime(timezone=True),
    )

    completed_at = db.Column(
        db.DateTime(timezone=True),
    )

    incident = db.relationship(
        "Incident",
        back_populates="response_decisions",
    )

    response_policy = db.relationship(
        "ResponsePolicy",
        back_populates="response_decisions",
    )

    response_connector = db.relationship(
        "ResponseConnector",
        back_populates="response_decisions",
    )

    decided_by_user = db.relationship(
        "User",
        foreign_keys=[decided_by_user_id],
        back_populates="response_decisions",
    )

    incident_actions = db.relationship(
        "IncidentAction",
        back_populates="response_decision",
    )