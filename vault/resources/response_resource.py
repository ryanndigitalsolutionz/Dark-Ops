from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.incident import Incident
from models.response_connector import ResponseConnector
from models.response_decision import ResponseDecision
from models.response_policy import ResponsePolicy
from models.team_member import TeamMember
from models.team_owner import TeamOwner
from schemas.response_decision_schema import ResponseDecisionSchema
from api.authentication.authentication import get_current_user


decision_schema = ResponseDecisionSchema()
decisions_schema = ResponseDecisionSchema(many=True)


def _can_access_team(user_id, team_id):
    return bool(
        TeamOwner.query.filter_by(
            team_id=team_id,
            user_id=user_id,
        ).first()
        or TeamMember.query.filter_by(
            team_id=team_id,
            user_id=user_id,
            status="active",
        ).first()
    )


def _can_access_incident(user_id, incident):
    application = incident.application

    if application.owner_user_id == user_id:
        return True

    return bool(
        application.team_id
        and _can_access_team(user_id, application.team_id)
    )


def _belongs_to_incident_context(policy, application):
    if application.owner_user_id:
        return (
            policy.owner_user_id == application.owner_user_id
            and policy.team_id is None
        )

    return (
        application.team_id is not None
        and policy.team_id == application.team_id
        and policy.owner_user_id is None
    )


def _connector_belongs_to_incident_context(connector, application):
    if application.owner_user_id:
        return (
            connector.owner_user_id == application.owner_user_id
            and connector.team_id is None
        )

    return (
        application.team_id is not None
        and connector.team_id == application.team_id
        and connector.owner_user_id is None
    )


class ResponseResource(Resource):
    def get(self, incident_id, decision_id=None):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        incident = db.session.get(Incident, incident_id)

        if not incident or not _can_access_incident(user.id, incident):
            return {"error": "Incident not found or access denied."}, 404

        if decision_id:
            decision = ResponseDecision.query.filter_by(
                id=decision_id,
                incident_id=incident_id,
            ).first()

            if not decision:
                return {"error": "Response decision not found."}, 404

            return decision_schema.dump(decision), 200

        decisions = (
            ResponseDecision.query
            .filter_by(incident_id=incident_id)
            .order_by(ResponseDecision.created_at.asc())
            .all()
        )

        return {"items": decisions_schema.dump(decisions)}, 200

    def post(self, incident_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        incident = db.session.get(Incident, incident_id)

        if not incident or not _can_access_incident(user.id, incident):
            return {"error": "Incident not found or access denied."}, 404

        data = request.get_json() or {}

        try:
            loaded = decision_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        application = incident.application
        policy = None
        connector = None

        if loaded.get("policy_id"):
            policy = db.session.get(
                ResponsePolicy,
                loaded["policy_id"],
            )

            if not policy or not _belongs_to_incident_context(
                policy,
                application,
            ):
                return {
                    "error": "Response policy does not belong to this security context."
                }, 400

        if loaded.get("connector_id"):
            connector = db.session.get(
                ResponseConnector,
                loaded["connector_id"],
            )

            if not connector or not _connector_belongs_to_incident_context(
                connector,
                application,
            ):
                return {
                    "error": "Response connector does not belong to this security context."
                }, 400

        decision = ResponseDecision(
            incident_id=incident_id,
            policy_id=policy.id if policy else None,
            connector_id=connector.id if connector else None,
            action_type=loaded["action_type"],
            execution_mode=loaded["execution_mode"],
            target_scope=loaded["target_scope"],
            target=loaded.get("target"),
            status="pending",
            rationale=loaded.get("rationale"),
            decided_by_user_id=user.id,
        )

        db.session.add(decision)
        db.session.commit()

        return decision_schema.dump(decision), 201

    def patch(self, incident_id, decision_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        incident = db.session.get(Incident, incident_id)

        if not incident or not _can_access_incident(user.id, incident):
            return {"error": "Incident not found or access denied."}, 404

        decision = ResponseDecision.query.filter_by(
            id=decision_id,
            incident_id=incident_id,
        ).first()

        if not decision:
            return {"error": "Response decision not found."}, 404

        data = request.get_json() or {}

        try:
            loaded = decision_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        for field in {"rationale", "target"}:
            if field in loaded:
                setattr(decision, field, loaded[field])

        db.session.commit()

        return decision_schema.dump(decision), 200
