import uuid
from datetime import datetime, timezone

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.team import Team
from models.team_owner import TeamOwner
from schemas.team_schema import TeamSchema
from models.team_member import TeamMember


team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)


class TeamResource(Resource):
    @jwt_required()
    def get(self, team_id=None):
        user_id = get_jwt_identity()

        if team_id:
            team = (
                Team.query
                .join(Team.members)
                .filter(Team.id == team_id)
                .filter_by(user_id=user_id, status="active")
                .first()
            )

            if not team:
                return {"error": "Team not found or access denied."}, 404

            return team_schema.dump(team), 200

        teams = (
            Team.query
            .join(Team.members)
            .filter(TeamMember.user_id == user_id, TeamMember.status == "active")
            .order_by(Team.created_at.desc())
            .all()
        )

        return {"items": teams_schema.dump(teams)}, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json() or {}

        try:
            loaded = team_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        if Team.query.filter_by(slug=loaded["slug"]).first():
            return {"error": "That team slug is already in use."}, 409

        team = Team(
            team_id=f"TM-{uuid.uuid4().hex[:16].upper()}",
            team_display_name=loaded["team_display_name"],
            slug=loaded["slug"],
            description=loaded.get("description"),
            status=loaded.get("status", "active"),
            live_access_status=loaded.get("live_access_status", "inactive"),
            created_by_user_id=user_id,
        )

        db.session.add(team)
        db.session.flush()

        owner = TeamOwner(
            team_id=team.id,
            user_id=user_id,
            assigned_by_user_id=user_id,
            status="active",
        )

        db.session.add(owner)
        db.session.commit()

        return team_schema.dump(team), 201

    @jwt_required()
    def patch(self, team_id):
        user_id = get_jwt_identity()

        team = (
            Team.query
            .join(Team.members)
            .filter(Team.id == team_id)
            .filter_by(user_id=user_id, status="active")
            .first()
        )

        if not team:
            return {"error": "Team not found or access denied."}, 404

        data = request.get_json() or {}

        try:
            loaded = team_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        for field, value in loaded.items():
            if field not in {"id", "team_id", "created_by_user_id"}:
                setattr(team, field, value)

        db.session.commit()

        return team_schema.dump(team), 200

    @jwt_required()
    def delete(self, team_id):
        user_id = get_jwt_identity()

        team = (
            Team.query
            .join(Team.members)
            .filter(Team.id == team_id)
            .filter_by(user_id=user_id, status="active")
            .first()
        )

        if not team:
            return {"error": "Team not found or access denied."}, 404

        owner = TeamOwner.query.filter_by(
            team_id=team.id,
            user_id=user_id,
            status="active",
        ).first()

        if not owner:
            return {"error": "Owner access is required."}, 403

        team.status = "terminated"
        team.terminated_at = datetime.now(timezone.utc)
        db.session.commit()

        return {"message": "Team terminated successfully."}, 200
