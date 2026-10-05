import uuid
from datetime import datetime, timezone
from extensions import db


class IncidentAction(db.Model):
    __tablename__ = "incident_action"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = db.Column(db.String(36), db.ForeignKey("incident.id"), nullable=False, index=True)
    response_decision_id = db.Column(db.String(36), db.ForeignKey("response_decision.id"), index=True)
    triggered_by_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), index=True)
    attempt_number = db.Column(db.Integer, nullable=False, default=1)
    action_type = db.Column(db.String(150), nullable=False, index=True)
    target = db.Column(db.Text)
    status = db.Column(db.String(30), nullable=False, default="pending", index=True)
    parameters = db.Column(db.JSON)
    result = db.Column(db.JSON)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    started_at = db.Column(db.DateTime(timezone=True))
    completed_at = db.Column(db.DateTime(timezone=True))

    incident = db.relationship("Incident", back_populates="actions")
    response_decision = db.relationship("ResponseDecision", back_populates="incident_actions")
    response_connector = db.relationship("ResponseConnector", back_populates="incident_actions")
    triggered_by = db.relationship("User", back_populates="incident_actions")

    __table_args__ = (
        db.CheckConstraint("attempt_number >= 1", name="ck_incident_action_attempt_number"),
    )
