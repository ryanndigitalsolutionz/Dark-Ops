from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.response_connector import ResponseConnector
from models.team_member import TeamMember
from models.team_owner import TeamOwner
from schemas.response_connector_schema import ResponseConnectorSchema
from api.authentication.authentication import get_current_user


connector_schema = ResponseConnectorSchema()
connectors_schema = ResponseConnectorSchema(many=True)


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


class ResponseConnectorResource(Resource):
    def get(self, team_id=None, connector_id=None):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        if team_id:
            if not _can_access_team(user.id, team_id):
                return {"error": "Team not found or access denied."}, 404

            query = ResponseConnector.query.filter_by(
                team_id=team_id,
                owner_user_id=None,
            )
        else:
            query = ResponseConnector.query.filter_by(
                owner_user_id=user.id,
                team_id=None,
            )

        if connector_id:
            connector = query.filter(
                ResponseConnector.id == connector_id
            ).first()

            if not connector:
                return {"error": "Response connector not found."}, 404

            return connector_schema.dump(connector), 200

        connectors = query.order_by(
            ResponseConnector.created_at.desc()
        ).all()

        return {"items": connectors_schema.dump(connectors)}, 200

    def post(self, team_id=None):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        if team_id:
            if not _can_access_team(user.id, team_id):
                return {"error": "Team not found or access denied."}, 404

            owner_user_id = None
        else:
            owner_user_id = user.id

        data = request.get_json() or {}

        try:
            loaded = connector_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        connector = ResponseConnector(
            owner_user_id=owner_user_id,
            team_id=team_id,
            created_by_user_id=user.id,
            name=loaded["name"],
            type=loaded["type"],
            base_url=loaded.get("base_url"),
            configuration_encrypted=loaded.get(
                "configuration_encrypted"
            ),
            status=loaded.get("status", "inactive"),
            metadata=loaded.get("metadata"),
        )

        db.session.add(connector)
        db.session.commit()

        return connector_schema.dump(connector), 201

    def patch(self, team_id, connector_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        query = ResponseConnector.query.filter_by(
            id=connector_id
        )

        if team_id:
            if not _can_access_team(user.id, team_id):
                return {"error": "Team not found or access denied."}, 404

            query = query.filter_by(
                team_id=team_id,
                owner_user_id=None,
            )
        else:
            query = query.filter_by(
                owner_user_id=user.id,
                team_id=None,
            )

        connector = query.first()

        if not connector:
            return {"error": "Response connector not found."}, 404

        data = request.get_json() or {}

        try:
            loaded = connector_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        protected = {
            "id",
            "owner_user_id",
            "team_id",
            "created_by_user_id",
        }

        for field, value in loaded.items():
            if field not in protected:
                setattr(connector, field, value)

        db.session.commit()

        return connector_schema.dump(connector), 200

    def delete(self, team_id, connector_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        query = ResponseConnector.query.filter_by(
            id=connector_id
        )

        if team_id:
            if not _can_access_team(user.id, team_id):
                return {"error": "Team not found or access denied."}, 404

            query = query.filter_by(
                team_id=team_id,
                owner_user_id=None,
            )
        else:
            query = query.filter_by(
                owner_user_id=user.id,
                team_id=None,
            )

        connector = query.first()

        if not connector:
            return {"error": "Response connector not found."}, 404

        connector.status = "revoked"
        db.session.commit()

        return {"message": "Response connector revoked successfully."}, 200
