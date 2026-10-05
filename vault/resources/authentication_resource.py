from flask import make_response, request
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash

from api.authentication.authentication import (
    AuthenticationError,
    TurnstileVerificationError,
    authenticate_credentials,
    authenticate_session,
    create_authenticated_session,
    get_current_user,
    set_session_cookie,
    verify_registration_challenge,
)
from extensions import db
from models.profile import Profile
from models.user import User
from schemas.authentication_schema import (
    authentication_response_schema,
    login_schema,
    register_schema,
)


def _generate_darkops_id():
    import secrets
    import string

    alphabet = string.ascii_lowercase + string.digits

    while True:
        darkops_id = "UR_" + "".join(secrets.choice(alphabet) for _ in range(5)) + ";"

        if not User.query.filter_by(darkops_id=darkops_id).first():
            return darkops_id


def _user_payload(user):
    profile = Profile.query.filter_by(user_id=user.id).first()

    return {
        "id": user.id,
        "darkops_id": user.darkops_id,
        "email": user.email,
        "username": user.username,
        "phone_number": user.phone_number,
        "email_verified_at": user.email_verified_at,
        "phone_verified_at": user.phone_verified_at,
        "status": user.status,
        "profile": (
            {
                "first_name": profile.first_name,
                "surname": profile.surname,
                "last_name": profile.last_name,
                "display_name": profile.display_name,
                "avatar_url": profile.avatar_url,
                "bio": profile.bio,
            }
            if profile
            else None
        ),
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "last_login_at": user.last_login_at,
    }


class AuthenticationResource(Resource):
    def post(self):
        data = request.get_json() or {}

        try:
            loaded = register_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        try:
            verify_registration_challenge(
                loaded["turnstile_token"],
            )
        except TurnstileVerificationError as error:
            return {
                "success": False,
                "message": str(error),
            }, 400

        email = loaded["email"].strip().lower()
        username = loaded["username"].strip().lower()
        phone_number = loaded["phone_number"].strip()

        if User.query.filter_by(email=email).first():
            return {
                "success": False,
                "message": "An account with that email already exists.",
            }, 409

        if User.query.filter_by(username=username).first():
            return {
                "success": False,
                "message": "That username is already in use.",
            }, 409

        if phone_number and User.query.filter_by(
            phone_number=phone_number
        ).first():
            return {
                "success": False,
                "message": "That phone number is already in use.",
            }, 409

        user = User(
            darkops_id=_generate_darkops_id(),
            email=email,
            username=username,
            phone_number=phone_number,
            password_hash=generate_password_hash(loaded["password"]),
            security_question=loaded["security_question"],
            security_answer_hash=generate_password_hash(
                loaded["security_answer"]
            ),
            status="active",
            email_verified_at=None,
            phone_verified_at=None,
        )

        db.session.add(user)
        db.session.flush()

        profile = Profile(
            user_id=user.id,
            first_name=loaded["first_name"],
            surname=loaded["surname"],
            last_name=loaded["last_name"],
            display_name=loaded["display_name"],
        )

        db.session.add(profile)
        db.session.commit()

        try:
            session, raw_session_token = create_authenticated_session(user)
        except AuthenticationError as error:
            db.session.rollback()
            return {
                "success": False,
                "message": str(error),
            }, 400

        response_data = authentication_response_schema.dump(
            {
                "success": True,
                "message": "Account created successfully.",
                "user": _user_payload(user),
            }
        )

        response = make_response(response_data, 201)
        set_session_cookie(
            response,
            raw_session_token,
            session,
        )

        return response

    def get(self):
        user = authenticate_session(touch=True)

        if not user:
            return {
                "success": False,
                "message": "Authentication is required.",
            }, 401

        return {
            "success": True,
            "user": _user_payload(user),
        }, 200

    def put(self):
        data = request.get_json() or {}

        try:
            loaded = login_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        identifier = loaded["login"].strip().lower()

        try:
            user = authenticate_credentials(
                identifier=identifier,
                password=loaded["password"],
                turnstile_token=loaded["turnstile_token"],
            )
        except TurnstileVerificationError as error:
            return {
                "success": False,
                "message": str(error),
            }, 400
        except AuthenticationError as error:
            return {
                "success": False,
                "message": str(error),
            }, 401

        if not user:
            return {
                "success": False,
                "message": "Invalid credentials.",
            }, 401

        try:
            session, raw_session_token = create_authenticated_session(user)
        except AuthenticationError as error:
            return {
                "success": False,
                "message": str(error),
            }, 400

        response_data = authentication_response_schema.dump(
            {
                "success": True,
                "message": "Authentication successful.",
                "user": _user_payload(user),
            }
        )

        response = make_response(response_data, 200)
        set_session_cookie(
            response,
            raw_session_token,
            session,
        )

        return response
