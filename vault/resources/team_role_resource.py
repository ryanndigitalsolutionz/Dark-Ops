from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.team import Team
from models.team_member import TeamMember
from models.team_role import TeamRole
from schemas.team_role_schema import TeamRoleSchema


role_schema = TeamRoleSchema()
roles_schema = TeamRoleSchema(many=True)


def _member(team_id, user_id):
    return TeamMember.query.filter_by(
        team_id=team_id,
        user_id=user_id,
        status="active",
    ).first()


class TeamRoleResource(Resource):
    @jwt_required()
    def get(self, team_id, role_id=None):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        if role_id:
            role = TeamRole.query.filter_by(
                id=role_id,
                team_id=team_id,
            ).first()

            if not role:
                return {"error": "Role not found."}, 404

            return role_schema.dump(role), 200

        roles = TeamRole.query.filter_by(team_id=team_id).order_by(TeamRole.name.asc()).all()

        return {"items": roles_schema.dump(roles)}, 200

    @jwt_required()
    def post(self, team_id):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        team = db.session.get(Team, team_id)

        if not team or team.status != "active":
            return {"error": "Team not found."}, 404

        data = request.get_json() or {}

        try:
            loaded = role_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        if TeamRole.query.filter_by(team_id=team_id, name=loaded["name"]).first():
            return {"error": "A role with that name already exists in this team."}, 409

        role = TeamRole(
            team_id=team_id,
            name=loaded["name"],
            description=loaded.get("description"),
            is_system_role=loaded.get("is_system_role", False),
            permissions=loaded.get("permissions", {}),
            console_layout=loaded.get("console_layout"),
        )

        db.session.add(role)
        db.session.commit()

        return role_schema.dump(role), 201

    @jwt_required()
    def patch(self, team_id, role_id):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        role = TeamRole.query.filter_by(
            id=role_id,
            team_id=team_id,
        ).first()

        if not role:
            return {"error": "Role not found."}, 404

        data = request.get_json() or {}

        try:
            loaded = role_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        for field, value in loaded.items():
            if field not in {"id", "team_id", "is_system_role"}:
                setattr(role, field, value)

        db.session.commit()

        return role_schema.dump(role), 200

    @jwt_required()
    def delete(self, team_id, role_id):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        role = TeamRole.query.filter_by(
            id=role_id,
            team_id=team_id,
        ).first()

        if not role:
            return {"error": "Role not found."}, 404

        if role.members:
            return {"error": "Role cannot be deleted while members are assigned to it."}, 409

        if role.is_system_role:
            return {"error": "System roles cannot be deleted."}, 403

        db.session.delete(role)
        db.session.commit()

        return {"message": "Role deleted successfully."}, 200
