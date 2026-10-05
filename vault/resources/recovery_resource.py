from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.incident import Incident
from models.recovery_operation import RecoveryOperation
from models.team_member import TeamMember
from models.team_owner import TeamOwner
from schemas.recovery_operation_schema import RecoveryOperationSchema
from api.authentication.authentication import get_current_user


recovery_schema = RecoveryOperationSchema()
recoveries_schema = RecoveryOperationSchema(many=True)


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


class RecoveryResource(Resource):
    def get(self, incident_id, recovery_id=None):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        incident = db.session.get(Incident, incident_id)

        if not incident or not _can_access_incident(user.id, incident):
            return {"error": "Incident not found or access denied."}, 404

        if recovery_id:
            recovery = RecoveryOperation.query.filter_by(
                id=recovery_id,
                incident_id=incident_id,
            ).first()

            if not recovery:
                return {"error": "Recovery operation not found."}, 404

            return recovery_schema.dump(recovery), 200

        recoveries = (
            RecoveryOperation.query
            .filter_by(incident_id=incident_id)
            .order_by(RecoveryOperation.created_at.asc())
            .all()
        )

        return {"items": recoveries_schema.dump(recoveries)}, 200

    def post(self, incident_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        incident = db.session.get(Incident, incident_id)

        if not incident or not _can_access_incident(user.id, incident):
            return {"error": "Incident not found or access denied."}, 404

        data = request.get_json() or {}

        try:
            loaded = recovery_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        recovery = RecoveryOperation(
            incident_id=incident_id,
            initiated_by_user_id=user.id,
            actor_type="user",
            operation_type=loaded["operation_type"],
            target=loaded.get("target"),
            status="pending",
            parameters=loaded.get("parameters"),
        )

        db.session.add(recovery)
        db.session.commit()

        return recovery_schema.dump(recovery), 201
