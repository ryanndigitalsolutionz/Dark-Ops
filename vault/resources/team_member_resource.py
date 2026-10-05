from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.team_member import TeamMember
from models.team_owner import TeamOwner
from models.team_role import TeamRole
from schemas.team_member_schema import TeamMemberSchema


member_schema = TeamMemberSchema()
members_schema = TeamMemberSchema(many=True)


def _member(team_id, user_id):
    return TeamMember.query.filter_by(
        team_id=team_id,
        user_id=user_id,
        status="active",
    ).first()


def _owner(team_id, user_id):
    return TeamOwner.query.filter_by(
        team_id=team_id,
        user_id=user_id,
        status="active",
    ).first()


class TeamMemberResource(Resource):
    @jwt_required()
    def get(self, team_id, member_id=None):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        if member_id:
            member = TeamMember.query.filter_by(
                id=member_id,
                team_id=team_id,
            ).first()

            if not member:
                return {"error": "Team member not found."}, 404

            return member_schema.dump(member), 200

        members = (
            TeamMember.query
            .filter_by(team_id=team_id)
            .order_by(TeamMember.joined_at.asc())
            .all()
        )

        return {"items": members_schema.dump(members)}, 200

    @jwt_required()
    def patch(self, team_id, member_id):
        user_id = get_jwt_identity()

        if not _owner(team_id, user_id):
            return {"error": "Owner access is required."}, 403

        member = TeamMember.query.filter_by(
            id=member_id,
            team_id=team_id,
        ).first()

        if not member:
            return {"error": "Team member not found."}, 404

        data = request.get_json() or {}

        try:
            loaded = member_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        if "role_id" in loaded:
            role = TeamRole.query.filter_by(
                id=loaded["role_id"],
                team_id=team_id,
            ).first()

            if not role:
                return {"error": "Role does not belong to this team."}, 400

        for field, value in loaded.items():
            if field not in {"id", "team_id", "user_id"}:
                setattr(member, field, value)

        db.session.commit()

        return member_schema.dump(member), 200

    @jwt_required()
    def delete(self, team_id, member_id):
        user_id = get_jwt_identity()

        member = TeamMember.query.filter_by(
            id=member_id,
            team_id=team_id,
        ).first()

        if not member:
            return {"error": "Team member not found."}, 404

        is_self = member.user_id == user_id
        is_owner = _owner(team_id, user_id)

        if not is_self and not is_owner:
            return {"error": "Access denied."}, 403

        if _owner(team_id, member.user_id):
            active_owners = TeamOwner.query.filter_by(
                team_id=team_id,
                status="active",
            ).count()

            if active_owners <= 1:
                return {"error": "The final active team owner cannot be removed."}, 409

            ownership = TeamOwner.query.filter_by(
                team_id=team_id,
                user_id=member.user_id,
                status="active",
            ).first()

            if ownership:
                ownership.status = "removed"

        member.status = "left" if is_self else "removed"
        db.session.commit()

        return {"message": "Team membership updated successfully."}, 200
