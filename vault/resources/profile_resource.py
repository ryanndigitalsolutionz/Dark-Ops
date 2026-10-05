from flask import request
from flask_restful import Resource

from extensions import db
from models.profile import Profile
from schemas.profile_schema import ProfileSchema
from api.authentication.authentication import get_current_user


profile_schema = ProfileSchema()


class ProfileResource(Resource):
    def get(self):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        profile = Profile.query.filter_by(
            user_id=user.id
        ).first()

        if not profile:
            return {"error": "Profile not found."}, 404

        return profile_schema.dump(profile), 200

    def post(self):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        existing = Profile.query.filter_by(
            user_id=user.id
        ).first()

        if existing:
            return {"error": "Profile already exists."}, 409

        data = request.get_json() or {}
        loaded = profile_schema.load(data)

        profile = Profile(
            user_id=user.id,
            **loaded,
        )

        db.session.add(profile)
        db.session.commit()

        return profile_schema.dump(profile), 201

    def patch(self):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        profile = Profile.query.filter_by(
            user_id=user.id
        ).first()

        if not profile:
            return {"error": "Profile not found."}, 404

        data = request.get_json() or {}
        loaded = profile_schema.load(data, partial=True)

        for field, value in loaded.items():
            setattr(profile, field, value)

        db.session.commit()

        return profile_schema.dump(profile), 200
