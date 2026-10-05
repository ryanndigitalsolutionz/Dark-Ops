from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from extensions import db
from models.settings import Settings
from schemas.setting_schema import SettingSchema


setting_schema = SettingSchema()


class SettingResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        settings = Settings.query.filter_by(user_id=user_id).first()

        if not settings:
            return {"error": "Settings not found."}, 404

        return setting_schema.dump(settings), 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        existing = Settings.query.filter_by(user_id=user_id).first()

        if existing:
            return {"error": "Settings already exist."}, 409

        data = request.get_json() or {}
        loaded = setting_schema.load(data)

        settings = Settings(
            user_id=user_id,
            **loaded,
        )

        db.session.add(settings)
        db.session.commit()

        return setting_schema.dump(settings), 201

    @jwt_required()
    def patch(self):
        user_id = get_jwt_identity()
        settings = Settings.query.filter_by(user_id=user_id).first()

        if not settings:
            return {"error": "Settings not found."}, 404

        data = request.get_json() or {}
        loaded = setting_schema.load(data, partial=True)

        for field, value in loaded.items():
            if field not in {"user_id", "profile_id"}:
                setattr(settings, field, value)

        db.session.commit()

        return setting_schema.dump(settings), 200
