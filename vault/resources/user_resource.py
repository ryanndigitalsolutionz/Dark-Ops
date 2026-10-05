from flask import request
from flask_restful import Resource

from extensions import db
from models.user import User
from schemas.user_schema import UserSchema
from api.authentication.authentication import get_current_user


user_schema = UserSchema()


class UserResource(Resource):
    def get(self):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        return user_schema.dump(user), 200

    def patch(self):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        data = request.get_json() or {}

        if "username" in data:
            return {"error": "Username cannot be changed after registration."}, 409

        if "phone_number" in data:
            phone_number = data["phone_number"]
            phone_number = phone_number.strip() if isinstance(phone_number, str) else phone_number

            if phone_number != user.phone_number:
                existing = User.query.filter(
                    User.phone_number == phone_number,
                    User.id != user.id,
                ).first()

                if existing:
                    return {"error": "That phone number is already in use."}, 409

                user.phone_number = phone_number
                user.phone_verified_at = None

        db.session.commit()

        return user_schema.dump(user), 200
