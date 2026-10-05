import hashlib
import secrets
from datetime import datetime, timezone

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.api_key import ApiKey
from models.application import Application
from models.subscription import Subscription
from models.team_member import TeamMember
from schemas.api_key_schema import ApiKeySchema


api_key_schema = ApiKeySchema()
api_keys_schema = ApiKeySchema(many=True)


def _can_access(application, user_id):
    if application.owner_user_id == user_id:
        return True

    if application.team_id:
        return bool(
            TeamMember.query.filter_by(
                team_id=application.team_id,
                user_id=user_id,
                status="active",
            ).first()
        )

    return False


class ApiKeyResource(Resource):
    @jwt_required()
    def get(self, api_key_id=None):
        user_id = get_jwt_identity()

        if api_key_id:
            api_key = db.session.get(ApiKey, api_key_id)

            if not api_key:
                return {"error": "API key not found."}, 404

            if api_key.application and not _can_access(api_key.application, user_id):
                return {"error": "Access denied."}, 403

            if api_key.owner_user_id != user_id and not api_key.team_id:
                return {"error": "Access denied."}, 403

            return api_key_schema.dump(api_key), 200

        owned_keys = ApiKey.query.filter_by(owner_user_id=user_id).all()

        team_keys = (
            ApiKey.query
            .join(TeamMember, TeamMember.team_id == ApiKey.team_id)
            .filter(
                TeamMember.user_id == user_id,
                TeamMember.status == "active",
            )
            .all()
        )

        keys = {key.id: key for key in owned_keys + team_keys}

        return {"items": api_keys_schema.dump(list(keys.values()))}, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json() or {}

        try:
            loaded = api_key_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        application = db.session.get(Application, loaded["application_id"])

        if not application or not _can_access(application, user_id):
            return {"error": "Application not found or access denied."}, 404

        subscription = db.session.get(Subscription, loaded["subscription_id"])

        if not subscription:
            return {"error": "Subscription not found."}, 404

        if subscription.team_id != application.team_id:
            if subscription.owner_user_id != application.owner_user_id:
                return {"error": "Subscription is not authorized for this application."}, 403

        raw_secret = secrets.token_urlsafe(48)
        secret_hash = hashlib.sha256(raw_secret.encode()).hexdigest()
        secret_prefix = raw_secret[:12]

        public_key = f"do_pk_{secrets.token_urlsafe(24)}"

        api_key = ApiKey(
            owner_user_id=user_id,
            team_id=application.team_id,
            application_id=application.id,
            subscription_id=subscription.id,
            created_by_user_id=user_id,
            name=loaded["name"],
            mode=loaded["mode"],
            environment=loaded["environment"],
            public_key=public_key,
            secret_key_hash=secret_hash,
            secret_key_prefix=secret_prefix,
            public_scopes=loaded.get("public_scopes", {}),
            secret_scopes=loaded.get("secret_scopes", {}),
            status="active",
            expires_at=loaded.get("expires_at"),
        )

        db.session.add(api_key)
        db.session.commit()

        response = api_key_schema.dump(api_key)
        response["secret_key"] = raw_secret

        return response, 201

    @jwt_required()
    def patch(self, api_key_id):
        user_id = get_jwt_identity()
        api_key = db.session.get(ApiKey, api_key_id)

        if not api_key:
            return {"error": "API key not found."}, 404

        if api_key.owner_user_id != user_id:
            if not api_key.team_id:
                return {"error": "Access denied."}, 403

            membership = TeamMember.query.filter_by(
                team_id=api_key.team_id,
                user_id=user_id,
                status="active",
            ).first()

            if not membership:
                return {"error": "Access denied."}, 403

        data = request.get_json() or {}

        try:
            loaded = api_key_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        for field, value in loaded.items():
            if field not in {
                "id",
                "owner_user_id",
                "team_id",
                "application_id",
                "subscription_id",
                "created_by_user_id",
                "public_key",
                "secret_key_hash",
                "secret_key_prefix",
            }:
                setattr(api_key, field, value)

        db.session.commit()

        return api_key_schema.dump(api_key), 200

    @jwt_required()
    def delete(self, api_key_id):
        user_id = get_jwt_identity()
        api_key = db.session.get(ApiKey, api_key_id)

        if not api_key:
            return {"error": "API key not found."}, 404

        if api_key.owner_user_id != user_id:
            return {"error": "Only the key owner can revoke this API key."}, 403

        api_key.status = "revoked"
        api_key.revoked_at = datetime.now(timezone.utc)
        db.session.commit()

        return {"message": "API key revoked successfully."}, 200
