from datetime import datetime, timezone

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from api.authentication.authentication import get_current_user
from extensions import db
from models.application import Application
from models.incident import Incident
from models.team_member import TeamMember
from models.user import User
from schemas.incident_schema import IncidentSchema


incident_schema = IncidentSchema()
incidents_schema = IncidentSchema(many=True)


def _can_access_application(application, user):
    if not application or not user:
        return False

    if application.owner_user_id == user.id:
        return True

    if application.team_id:
        return bool(
            TeamMember.query.filter_by(
                team_id=application.team_id,
                user_id=user.id,
                status="active",
            ).first()
        )

    return False


def _user_can_manage_incident(user, application):
    if application.owner_user_id == user.id:
        return True

    if not application.team_id:
        return False

    from security.authorization import has_capability

    return has_capability(
        user,
        "incident.manage",
        team_id=application.team_id,
    )


def _user_can_view_incident(user, application):
    if application.owner_user_id == user.id:
        return True

    if not application.team_id:
        return False

    from security.authorization import has_capability

    return has_capability(
        user,
        "incident.view",
        team_id=application.team_id,
    )


def _can_assign_user(application, user_id):
    if not user_id:
        return True

    user = db.session.get(User, user_id)

    if not user or user.status != "active":
        return False

    if application.owner_user_id == user.id:
        return True

    if not application.team_id:
        return False

    return bool(
        TeamMember.query.filter_by(
            team_id=application.team_id,
            user_id=user.id,
            status="active",
        ).first()
    )


def _validate_transition(current_status, new_status):
    if current_status == new_status:
        return True

    allowed = {
        "open": {"investigating", "contained", "resolved"},
        "investigating": {"contained", "resolved"},
        "contained": {"resolved"},
        "resolved": {"closed"},
        "closed": set(),
    }

    return new_status in allowed.get(current_status, set())


class IncidentResource(Resource):
    def get(self, application_id, incident_id=None):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        application = db.session.get(
            Application,
            application_id,
        )

        if not application or not _can_access_application(application, user):
            return {
                "error": "Application not found or access denied."
            }, 404

        if not _user_can_view_incident(user, application):
            return {
                "error": "Insufficient permissions."
            }, 403

        if incident_id:
            incident = Incident.query.filter_by(
                id=incident_id,
                application_id=application_id,
            ).first()

            if not incident:
                return {"error": "Incident not found."}, 404

            return incident_schema.dump(incident), 200

        incidents = (
            Incident.query
            .filter_by(application_id=application_id)
            .order_by(Incident.created_at.desc())
            .all()
        )

        return {
            "items": incidents_schema.dump(incidents)
        }, 200

    def post(self, application_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        application = db.session.get(
            Application,
            application_id,
        )

        if not application or not _can_access_application(application, user):
            return {
                "error": "Application not found or access denied."
            }, 404

        if not _user_can_manage_incident(user, application):
            return {
                "error": "Insufficient permissions."
            }, 403

        data = request.get_json() or {}

        try:
            loaded = incident_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        assigned_to_user_id = loaded.get("assigned_to_user_id")

        if assigned_to_user_id and not _can_assign_user(
            application,
            assigned_to_user_id,
        ):
            return {
                "error": "Assigned user does not have access to this application."
            }, 400

        incident = Incident(
            application_id=application_id,
            title=loaded["title"],
            description=loaded.get("description"),
            severity=loaded["severity"],
            status="open",
            assigned_to_user_id=assigned_to_user_id,
            resolution=loaded.get("resolution"),
            metadata=loaded.get("metadata"),
        )

        db.session.add(incident)
        db.session.commit()

        return incident_schema.dump(incident), 201

    def patch(self, application_id, incident_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        application = db.session.get(
            Application,
            application_id,
        )

        if not application or not _can_access_application(application, user):
            return {
                "error": "Application not found or access denied."
            }, 404

        if not _user_can_manage_incident(user, application):
            return {
                "error": "Insufficient permissions."
            }, 403

        incident = Incident.query.filter_by(
            id=incident_id,
            application_id=application_id,
        ).first()

        if not incident:
            return {"error": "Incident not found."}, 404

        data = request.get_json() or {}

        try:
            loaded = incident_schema.load(
                data,
                partial=True,
            )
        except ValidationError as error:
            return {"errors": error.messages}, 400

        if "assigned_to_user_id" in loaded:
            if not _can_assign_user(
                application,
                loaded["assigned_to_user_id"],
            ):
                return {
                    "error": "Assigned user does not have access to this application."
                }, 400

        new_status = loaded.get("status")

        if new_status:
            if not _validate_transition(
                incident.status,
                new_status,
            ):
                return {
                    "error": (
                        f"Invalid incident transition: "
                        f"{incident.status} -> {new_status}."
                    )
                }, 400

        now = datetime.now(timezone.utc)

        if new_status == "contained" and not incident.contained_at:
            incident.contained_at = now

        if new_status == "resolved" and not incident.resolved_at:
            incident.resolved_at = now

        if new_status == "closed" and not incident.closed_at:
            incident.closed_at = now

        editable_fields = {
            "title",
            "description",
            "severity",
            "status",
            "assigned_to_user_id",
            "resolution",
            "metadata",
        }

        for field, value in loaded.items():
            if field in editable_fields:
                setattr(incident, field, value)

        db.session.commit()

        return incident_schema.dump(incident), 200
