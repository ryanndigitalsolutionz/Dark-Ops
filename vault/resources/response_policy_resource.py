from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.response_policy import ResponsePolicy
from models.team_member import TeamMember
from models.team_owner import TeamOwner
from schemas.response_policy_schema import ResponsePolicySchema
from api.authentication.authentication import get_current_user


policy_schema = ResponsePolicySchema()
policies_schema = ResponsePolicySchema(many=True)


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


class ResponsePolicyResource(Resource):
    def get(self, team_id=None, policy_id=None):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        if team_id:
            if not _can_access_team(user.id, team_id):
                return {"error": "Team not found or access denied."}, 404

            query = ResponsePolicy.query.filter_by(
                team_id=team_id,
                owner_user_id=None,
            )
        else:
            query = ResponsePolicy.query.filter_by(
                owner_user_id=user.id,
                team_id=None,
            )

        if policy_id:
            policy = query.filter(
                ResponsePolicy.id == policy_id
            ).first()

            if not policy:
                return {"error": "Response policy not found."}, 404

            return policy_schema.dump(policy), 200

        policies = query.order_by(
            ResponsePolicy.created_at.desc()
        ).all()

        return {"items": policies_schema.dump(policies)}, 200

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
            loaded = policy_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        policy = ResponsePolicy(
            owner_user_id=owner_user_id,
            team_id=team_id,
            created_by_user_id=user.id,
            name=loaded["name"],
            description=loaded.get("description"),
            execution_mode=loaded.get(
                "execution_mode",
                "approval_required",
            ),
            triggers=loaded.get("triggers"),
            rules=loaded.get("rules"),
            enabled=loaded.get("enabled", True),
        )

        db.session.add(policy)
        db.session.commit()

        return policy_schema.dump(policy), 201

    def patch(self, team_id, policy_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        query = ResponsePolicy.query.filter_by(id=policy_id)

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

        policy = query.first()

        if not policy:
            return {"error": "Response policy not found."}, 404

        data = request.get_json() or {}

        try:
            loaded = policy_schema.load(data, partial=True)
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
                setattr(policy, field, value)

        db.session.commit()

        return policy_schema.dump(policy), 200

    def delete(self, team_id, policy_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        query = ResponsePolicy.query.filter_by(id=policy_id)

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

        policy = query.first()

        if not policy:
            return {"error": "Response policy not found."}, 404

        db.session.delete(policy)
        db.session.commit()

        return {"message": "Response policy deleted successfully."}, 200
