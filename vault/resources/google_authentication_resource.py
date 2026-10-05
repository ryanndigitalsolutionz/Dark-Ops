from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource

from extensions import db
from models.user import User


class GoogleAuthenticationResource(Resource):
    def post(self):
        data = request.get_json() or {}
        google_subject = data.get("google_subject")
        email = data.get("email", "").strip().lower()
        username = data.get("username", "").strip()

        if not google_subject or not email:
            return {"error": "Google subject and email are required."}, 400

        user = User.query.filter_by(google_subject=google_subject).first()

        if not user:
            user = User.query.filter_by(email=email).first()

            if user:
                if user.google_subject and user.google_subject != google_subject:
                    return {"error": "This email is already linked to another Google identity."}, 409
                user.google_subject = google_subject
            else:
                if not username:
                    return {"error": "Username is required when creating a new account."}, 400

                if User.query.filter_by(username=username).first():
                    return {"error": "That username is already in use."}, 409

                user = User(
                    darkops_id=f"DO-{__import__('uuid').uuid4().hex[:16].upper()}",
                    email=email,
                    username=username,
                    google_subject=google_subject,
                    status="active",
                )
                db.session.add(user)

        db.session.commit()

        return {
            "message": "Google authentication successful.",
            "user": {
                "id": user.id,
                "darkops_id": user.darkops_id,
                "email": user.email,
                "username": user.username,
            },
            "access_token": create_access_token(identity=user.id),
            "refresh_token": create_refresh_token(identity=user.id),
        }, 200
