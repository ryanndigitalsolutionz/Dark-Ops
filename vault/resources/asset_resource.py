from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from api.authentication.authentication import get_current_user
from api.security.authorization import can_access_application, has_user_capability
from extensions import db
from models.asset import Asset
from models.application import Application
from schemas.asset_schema import AssetSchema, assets_schema


asset_schema = AssetSchema()


def _can_access(application, user_id):
    return can_access_application(application, user_id)


def _can_manage(application, user_id):
    if not _can_access(application, user_id):
        return False

    if application.team_id is None:
        return application.owner_user_id == user_id

    return has_user_capability(
        user_id,
        application.team_id,
        "asset.create",
    ) or has_user_capability(
        user_id,
        application.team_id,
        "asset.update",
    )


def _has_capability(application, user_id, capability):
    if not _can_access(application, user_id):
        return False

    if application.team_id is None:
        return application.owner_user_id == user_id

    return has_user_capability(
        user_id,
        application.team_id,
        capability,
    )


class AssetResource(Resource):
    def get(self, application_id, asset_id=None):
        user = get_current_user()

        if not user:
            return {"error": "Authentication is required."}, 401

        application = db.session.get(Application, application_id)

        if not application or not _has_capability(application, user.id, "asset.view"):
            return {"error": "Application not found or access denied."}, 404

        if asset_id:
            asset = Asset.query.filter_by(
                id=asset_id,
                application_id=application_id,
            ).first()

            if not asset:
                return {"error": "Asset not found."}, 404

            return asset_schema.dump(asset), 200

        assets = (
            Asset.query
            .filter_by(application_id=application_id)
            .order_by(Asset.created_at.desc())
            .all()
        )

        return {"items": assets_schema.dump(assets)}, 200

    def post(self, application_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication is required."}, 401

        application = db.session.get(Application, application_id)

        if not application or not _has_capability(application, user.id, "asset.create"):
            return {"error": "Application not found or asset creation is not allowed."}, 403

        data = request.get_json() or {}

        try:
            loaded = asset_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        existing = Asset.query.filter_by(
            application_id=application_id,
            identifier=loaded["identifier"],
        ).first()

        if existing:
            return {"error": "An asset with that identifier already exists."}, 409

        asset = Asset(
            application_id=application_id,
            name=loaded["name"],
            identifier=loaded["identifier"],
            type=loaded["type"],
            description=loaded.get("description"),
            metadata=loaded.get("metadata"),
        )

        db.session.add(asset)
        db.session.commit()

        return asset_schema.dump(asset), 201

    def patch(self, application_id, asset_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication is required."}, 401

        application = db.session.get(Application, application_id)

        if not application or not _has_capability(application, user.id, "asset.update"):
            return {"error": "Application not found or asset update is not allowed."}, 403

        asset = Asset.query.filter_by(
            id=asset_id,
            application_id=application_id,
        ).first()

        if not asset:
            return {"error": "Asset not found."}, 404

        data = request.get_json() or {}

        try:
            loaded = asset_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        protected_fields = {
            "id",
            "application_id",
            "status",
            "original_filename",
            "mime_type",
            "size_bytes",
            "storage_provider",
            "storage_key",
            "checksum_sha256",
            "analysis_status",
            "analysis_metadata",
            "last_analyzed_at",
            "created_at",
            "updated_at",
        }

        for field, value in loaded.items():
            if field not in protected_fields:
                setattr(asset, field, value)

        db.session.commit()

        return asset_schema.dump(asset), 200

    def delete(self, application_id, asset_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication is required."}, 401

        application = db.session.get(Application, application_id)

        if not application or not _has_capability(application, user.id, "asset.update"):
            return {"error": "Application not found or asset deletion is not allowed."}, 403

        asset = Asset.query.filter_by(
            id=asset_id,
            application_id=application_id,
        ).first()

        if not asset:
            return {"error": "Asset not found."}, 404

        asset.status = "inactive"
        db.session.commit()

        return {"message": "Asset deactivated successfully."}, 200
    