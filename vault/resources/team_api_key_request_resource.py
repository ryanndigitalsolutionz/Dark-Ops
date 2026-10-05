from decimal import Decimal

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.api_key import ApiKey
from models.team_api_key_request import TeamApiKeyRequest
from models.team_api_key_vote import TeamApiKeyVote
from models.team_member import TeamMember
from models.team_owner import TeamOwner
from schemas.team_api_key_request_schema import TeamApiKeyRequestSchema


request_schema = TeamApiKeyRequestSchema()
requests_schema = TeamApiKeyRequestSchema(many=True)


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


class TeamApiKeyRequestResource(Resource):
    @jwt_required()
    def get(self, team_id, request_id=None):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        if request_id:
            key_request = TeamApiKeyRequest.query.filter_by(
                id=request_id,
                team_id=team_id,
            ).first()

            if not key_request:
                return {"error": "API key request not found."}, 404

            return request_schema.dump(key_request), 200

        requests = (
            TeamApiKeyRequest.query
            .filter_by(team_id=team_id)
            .order_by(TeamApiKeyRequest.created_at.desc())
            .all()
        )

        return {"items": requests_schema.dump(requests)}, 200

    @jwt_required()
    def post(self, team_id):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        data = request.get_json() or {}

        try:
            loaded = request_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        key_request = TeamApiKeyRequest(
            team_id=team_id,
            application_id=loaded["application_id"],
            subscription_id=loaded["subscription_id"],
            requested_by_user_id=user_id,
            name=loaded["name"],
            mode=loaded["mode"],
            environment=loaded["environment"],
            reason=loaded.get("reason"),
            status="pending",
            vote_threshold=Decimal(str(loaded.get("vote_threshold", 60))),
        )

        db.session.add(key_request)
        db.session.commit()

        return request_schema.dump(key_request), 201

    @jwt_required()
    def patch(self, team_id, request_id):
        user_id = get_jwt_identity()

        key_request = TeamApiKeyRequest.query.filter_by(
            id=request_id,
            team_id=team_id,
        ).first()

        if not key_request:
            return {"error": "API key request not found."}, 404

        data = request.get_json() or {}
        action = data.get("action")

        if action == "vote":
            if not _member(team_id, user_id):
                return {"error": "Team access denied."}, 403

            if key_request.status != "pending":
                return {"error": "This request is no longer accepting votes."}, 409

            vote_percentage = data.get("vote_percentage")

            if vote_percentage is None:
                return {"error": "vote_percentage is required."}, 400

            try:
                vote_percentage = Decimal(str(vote_percentage))
            except Exception:
                return {"error": "vote_percentage must be numeric."}, 400

            if vote_percentage < 0 or vote_percentage > 100:
                return {"error": "vote_percentage must be between 0 and 100."}, 400

            vote = TeamApiKeyVote.query.filter_by(
                request_id=key_request.id,
                voter_user_id=user_id,
            ).first()

            if vote:
                vote.vote_percentage = vote_percentage
            else:
                vote = TeamApiKeyVote(
                    request_id=key_request.id,
                    team_id=team_id,
                    voter_user_id=user_id,
                    vote_percentage=vote_percentage,
                    decision="pending",
                )
                db.session.add(vote)

            db.session.flush()

            votes = TeamApiKeyVote.query.filter_by(
                request_id=key_request.id
            ).all()

            key_request.vote_count = len(votes)
            key_request.total_vote_percentage = sum(
                (Decimal(str(item.vote_percentage)) for item in votes),
                Decimal("0"),
            )

            if key_request.total_vote_percentage < key_request.vote_threshold:
                key_request.status = "rejected"
                key_request.owner_decision = "rejected"

            db.session.commit()

            return request_schema.dump(key_request), 200

        if action == "owner_decision":
            if not _owner(team_id, user_id):
                return {"error": "Owner access is required."}, 403

            decision = data.get("owner_decision")

            if decision not in {"approved", "rejected"}:
                return {"error": "owner_decision must be approved or rejected."}, 400

            if key_request.total_vote_percentage < key_request.vote_threshold:
                key_request.status = "rejected"
                key_request.owner_decision = "rejected"
                db.session.commit()
                return {
                    "error": "The request did not reach the required voting threshold.",
                    "request": request_schema.dump(key_request),
                }, 409

            key_request.owner_decision = decision
            key_request.reviewed_by_user_id = user_id
            key_request.status = decision
            key_request.completed_at = db.func.now()

            db.session.commit()

            return request_schema.dump(key_request), 200

        if action == "cancel":
            if key_request.requested_by_user_id != user_id and not _owner(team_id, user_id):
                return {"error": "Access denied."}, 403

            if key_request.status != "pending":
                return {"error": "Only pending requests can be cancelled."}, 409

            key_request.status = "cancelled"
            key_request.completed_at = db.func.now()
            db.session.commit()

            return request_schema.dump(key_request), 200

        return {"error": "Unsupported request action."}, 400
