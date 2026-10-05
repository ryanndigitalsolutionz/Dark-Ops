from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.team_member import TeamMember
from models.team_owner import TeamOwner
from models.user import User
from schemas.team_owner_schema import TeamOwnerSchema


owner_schema = TeamOwnerSchema()
owners_schema = TeamOwnerSchema(many=True)


def _owner(team_id, user_id):
    return TeamOwner.query.filter_by(
        team_id=team_id,
        user_id=user_id,
        status="active",
    ).first()


class TeamOwnerResource(Resource):
    @jwt_required()
    def get(self, team_id, owner_id=None):
        user_id = get_jwt_identity()

        if not _owner(team_id, user_id):
            return {"error": "Owner access is required."}, 403

        if owner_id:
            owner = TeamOwner.query.filter_by(
                id=owner_id,
                team_id=team_id,
            ).first()

            if not owner:
                return {"error": "Team owner not found."}, 404

            return owner_schema.dump(owner), 200

        owners = (
            TeamOwner.query
            .filter_by(team_id=team_id, status="active")
            .order_by(TeamOwner.assigned_at.asc())
            .all()
        )

        return {"items": owners_schema.dump(owners)}, 200

    @jwt_required()
    def post(self, team_id):
        user_id = get_jwt_identity()

        if not _owner(team_id, user_id):
            return {"error": "Owner access is required."}, 403

        data = request.get_json() or {}

        try:
            loaded = owner_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        target_user_id = loaded["user_id"]
        target_user = db.session.get(User, target_user_id)

        if not target_user:
            return {"error": "User not found."}, 404

        member = TeamMember.query.filter_by(
            team_id=team_id,
            user_id=target_user_id,
            status="active",
        ).first()

        if not member:
            return {"error": "Only active team members can become owners."}, 400

        existing = TeamOwner.query.filter_by(
            team_id=team_id,
            user_id=target_user_id,
            status="active",
        ).first()

        if existing:
            return {"error": "That user is already a team owner."}, 409

        owner = TeamOwner(
            team_id=team_id,
            user_id=target_user_id,
            assigned_by_user_id=user_id,
            status="active",
        )

        db.session.add(owner)
        db.session.commit()

        return owner_schema.dump(owner), 201

    @jwt_required()
    def delete(self, team_id, owner_id):
        user_id = get_jwt_identity()

        if not _owner(team_id, user_id):
            return {"error": "Owner access is required."}, 403

        owner = TeamOwner.query.filter_by(
            id=owner_id,
            team_id=team_id,
            status="active",
        ).first()

        if not owner:
            return {"error": "Active team owner not found."}, 404

        active_owner_count = TeamOwner.query.filter_by(
            team_id=team_id,
            status="active",
        ).count()

        if active_owner_count <= 1:
            return {"error": "The final active team owner cannot be removed."}, 409

        owner.status = "removed"
        db.session.commit()

        return {"message": "Team ownership removed successfully."}, 200
