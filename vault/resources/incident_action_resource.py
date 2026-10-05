from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.incident import Incident
from models.incident_action import IncidentAction
from schemas.incident_action_schema import IncidentActionSchema


action_schema = IncidentActionSchema()
actions_schema = IncidentActionSchema(many=True)


class IncidentActionResource(Resource):
    @jwt_required()
    def get(self, incident_id, action_id=None):
        incident = db.session.get(Incident, incident_id)

        if not incident:
            return {"error": "Incident not found."}, 404

        if action_id:
            action = IncidentAction.query.filter_by(
                id=action_id,
                incident_id=incident_id,
            ).first()

            if not action:
                return {"error": "Incident action not found."}, 404

            return action_schema.dump(action), 200

        actions = (
            IncidentAction.query
            .filter_by(incident_id=incident_id)
            .order_by(IncidentAction.created_at.asc())
            .all()
        )

        return {"items": actions_schema.dump(actions)}, 200

    @jwt_required()
    def post(self, incident_id):
        user_id = get_jwt_identity()
        incident = db.session.get(Incident, incident_id)

        if not incident:
            return {"error": "Incident not found."}, 404

        data = request.get_json() or {}

        try:
            loaded = action_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        action = IncidentAction(
            incident_id=incident_id,
            response_decision_id=loaded.get("response_decision_id"),
            triggered_by_user_id=loaded.get("triggered_by_user_id", user_id),
            attempt_number=loaded.get("attempt_number", 1),
            action_type=loaded["action_type"],
            target=loaded.get("target"),
            status=loaded.get("status", "pending"),
            parameters=loaded.get("parameters"),
            result=loaded.get("result"),
            error=loaded.get("error"),
            started_at=loaded.get("started_at"),
            completed_at=loaded.get("completed_at"),
        )

        db.session.add(action)
        db.session.commit()

        return action_schema.dump(action), 201

    @jwt_required()
    def patch(self, incident_id, action_id):
        action = IncidentAction.query.filter_by(
            id=action_id,
            incident_id=incident_id,
        ).first()

        if not action:
            return {"error": "Incident action not found."}, 404

        data = request.get_json() or {}

        try:
            loaded = action_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        for field, value in loaded.items():
            if field not in {
                "id",
                "incident_id",
                "response_decision_id",
                "triggered_by_user_id",
                "attempt_number",
            }:
                setattr(action, field, value)

        db.session.commit()

        return action_schema.dump(action), 200
