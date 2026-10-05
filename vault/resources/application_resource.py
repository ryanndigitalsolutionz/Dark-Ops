import re
from datetime import datetime, timezone

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from api.authentication.authentication import get_current_user
from api.security.authorization import can_access_application, has_team_access, has_user_capability
from sqlalchemy import or_
from extensions import db
from models.application import Application
from models.team_member import TeamMember
from models.team_owner import TeamOwner
from schemas.application_schema import ApplicationSchema, applications_schema


application_schema = ApplicationSchema()


def _slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "application"


def _unique_slug(name, environment, owner_user_id=None, team_id=None):
    base = _slugify(name)
    slug = base
    counter = 2

    while Application.query.filter_by(
        owner_user_id=owner_user_id,
        team_id=team_id,
        slug=slug,
        environment=environment,
    ).first():
        slug = f"{base}-{counter}"
        counter += 1

    return slug


def _has_application_capability(application, user_id, capability=None):
    if not can_access_application(application, user_id):
        return False

    if application.team_id is None:
        return application.owner_user_id == user_id

    return capability is None or has_user_capability(
        user_id,
        application.team_id,
        capability,
    )


def _accessible_applications(user_id):
    team_ids = {
        team_id
        for team_id, in db.session.query(TeamMember.team_id).filter_by(
            user_id=user_id,
            status="active",
        ).all()
    }

    team_ids.update(
        team_id
        for team_id, in db.session.query(TeamOwner.team_id).filter_by(
            user_id=user_id,
        ).all()
    )

    filters = [Application.owner_user_id == user_id]

    if team_ids:
        filters.append(Application.team_id.in_(team_ids))

    candidates = Application.query.filter(or_(*filters)).all()

    return [
        application
        for application in candidates
        if _has_application_capability(
            application,
            user_id,
            "application.view",
        )
    ]


class ApplicationResource(Resource):
    def get(self, application_id=None):
        user = get_current_user()

        if not user:
            return {"error": "Authentication is required."}, 401

        if application_id:
            application = db.session.get(Application, application_id)

            if not application or not _has_application_capability(
                application,
                user.id,
                "application.view",
            ):
                return {"error": "Application not found or access denied."}, 404

            return application_schema.dump(application), 200

        applications = sorted(
            _accessible_applications(user.id),
            key=lambda item: item.created_at or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )

        return {"items": applications_schema.dump(applications)}, 200

    def post(self, team_id=None):
        user = get_current_user()

        if not user:
            return {"error": "Authentication is required."}, 401

        if team_id:
            if not has_team_access(user.id, team_id):
                return {"error": "Team access is required."}, 403

            if not has_user_capability(
                user.id,
                team_id,
                "application.manage",
            ):
                return {"error": "Application management capability is required."}, 403

        data = request.get_json() or {}

        try:
            loaded = application_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        environment = loaded.get("environment", "test")

        owner_user_id = None if team_id else user.id

        application = Application(
            owner_user_id=owner_user_id,
            team_id=team_id,
            created_by_user_id=user.id,
            name=loaded["name"],
            slug=_unique_slug(
                loaded["name"],
                environment,
                owner_user_id=owner_user_id,
                team_id=team_id,
            ),
            type=loaded["type"],
            environment=environment,
            status="disconnected",
            authorized_primary_url=loaded["authorized_primary_url"],
            base_url=loaded.get("base_url"),
            description=loaded.get("description"),
            webhook_url=loaded.get("webhook_url"),
            webhook_events=loaded.get("webhook_events"),
        )

        db.session.add(application)
        db.session.commit()

        return application_schema.dump(application), 201

    def patch(self, application_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication is required."}, 401

        application = db.session.get(Application, application_id)

        if not application:
            return {"error": "Application not found."}, 404

        if not _has_application_capability(
            application,
            user.id,
        ):
            return {"error": "Application not found or access denied."}, 404

        data = request.get_json() or {}

        try:
            loaded = application_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        protection_fields = {
            "authorized_primary_url",
            "base_url",
        }

        management_fields = {
            "name",
            "type",
            "environment",
            "description",
            "webhook_url",
            "webhook_events",
        }

        touched_fields = set(loaded)

        if touched_fields & protection_fields:
            if not _has_application_capability(
                application,
                user.id,
                "application.configure_protection",
            ):
                return {"error": "Application protection capability is required."}, 403

        if touched_fields & management_fields and not (
            touched_fields & protection_fields
        ):
            if not _has_application_capability(
                application,
                user.id,
                "application.manage",
            ):
                return {"error": "Application management capability is required."}, 403

        protected_fields = {
            "id",
            "owner_user_id",
            "team_id",
            "created_by_user_id",
            "slug",
            "status",
            "detection_state",
            "webhook_secret_hash",
            "webhook_secret_prefix",
            "webhook_active",
            "webhook_last_delivery_at",
            "connected_at",
            "disconnected_at",
            "created_at",
            "updated_at",
        }

        for field, value in loaded.items():
            if field not in protected_fields:
                setattr(application, field, value)

        db.session.commit()

        return application_schema.dump(application), 200

    def delete(self, application_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication is required."}, 401

        application = db.session.get(Application, application_id)

        if not application:
            return {"error": "Application not found."}, 404

        if not _has_application_capability(
            application,
            user.id,
            "application.disconnect",
        ):
            return {"error": "Application disconnect capability is required."}, 403

        application.status = "disconnected"
        application.disconnected_at = datetime.now(timezone.utc)
        db.session.commit()

        return {"message": "Application disconnected successfully."}, 200
