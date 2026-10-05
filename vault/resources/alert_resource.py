from datetime import datetime, timezone

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from api.authentication.authentication import get_current_user
from api.security.authorization import can_access_application, has_user_capability
from extensions import db
from models.alert import Alert
from models.application import Application
from models.asset import Asset
from models.event import Event
from models.incident import Incident
from models.team_member import TeamMember
from schemas.alert_schema import AlertSchema, alerts_schema


alert_schema = AlertSchema()


def _can_access(application, user_id):
    return can_access_application(application, user_id)


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


def _valid_assignee(application, user_id):
    if not user_id:
        return True

    if not _can_access(application, user_id):
        return False

    if application.team_id is None:
        return application.owner_user_id == user_id

    membership = TeamMember.query.filter_by(
        team_id=application.team_id,
        user_id=user_id,
        status="active",
    ).first()

    return bool(
        membership
        and has_user_capability(
            user_id,
            application.team_id,
            "alert.view",
        )
    )


def _related_to_application(model, object_id, application_id):
    if not object_id:
        return True

    return db.session.query(model.id).filter_by(
        id=object_id,
        application_id=application_id,
    ).first() is not None


class AlertResource(Resource):
    def get(self, application_id, alert_id=None):
        user = get_current_user()

        if not user:
            return {"error": "Authentication is required."}, 401

        application = db.session.get(Application, application_id)

        if not application or not _has_capability(
            application,
            user.id,
            "alert.view",
        ):
            return {"error": "Application not found or access denied."}, 404

        if alert_id:
            alert = Alert.query.filter_by(
                id=alert_id,
                application_id=application_id,
            ).first()

            if not alert:
                return {"error": "Alert not found."}, 404

            return alert_schema.dump(alert), 200

        alerts = (
            Alert.query
            .filter_by(application_id=application_id)
            .order_by(Alert.created_at.desc())
            .all()
        )

        return {"items": alerts_schema.dump(alerts)}, 200

    def post(self, application_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication is required."}, 401

        application = db.session.get(Application, application_id)

        if not application or not _has_capability(
            application,
            user.id,
            "alert.create",
        ):
            return {"error": "Application not found or alert creation is not allowed."}, 403

        data = request.get_json() or {}

        try:
            loaded = alert_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        if not _valid_assignee(
            application,
            loaded.get("assigned_to_user_id"),
        ):
            return {"error": "Assigned user cannot access this application alert."}, 400

        if not _related_to_application(
            Asset,
            loaded.get("asset_id"),
            application_id,
        ):
            return {"error": "Asset does not belong to this application."}, 400

        if not _related_to_application(
            Event,
            loaded.get("event_id"),
            application_id,
        ):
            return {"error": "Event does not belong to this application."}, 400

        if not _related_to_application(
            Incident,
            loaded.get("incident_id"),
            application_id,
        ):
            return {"error": "Incident does not belong to this application."}, 400

        if loaded.get("assigned_to_user_id") and not _has_capability(
            application,
            user.id,
            "alert.assign",
        ):
            return {"error": "Alert assignment capability is required."}, 403

        alert = Alert(
            application_id=application_id,
            asset_id=loaded.get("asset_id"),
            event_id=loaded.get("event_id"),
            incident_id=loaded.get("incident_id"),
            created_by_user_id=user.id,
            origin="user",
            title=loaded["title"],
            description=loaded.get("description"),
            alert_type=loaded["alert_type"],
            severity=loaded["severity"],
            status="open",
            assigned_to_user_id=loaded.get("assigned_to_user_id"),
            metadata=loaded.get("metadata"),
        )

        db.session.add(alert)
        db.session.commit()

        return alert_schema.dump(alert), 201

    def patch(self, application_id, alert_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication is required."}, 401

        application = db.session.get(Application, application_id)

        if not application or not _can_access(
            application,
            user.id,
        ):
            return {"error": "Application not found or access denied."}, 404

        alert = Alert.query.filter_by(
            id=alert_id,
            application_id=application_id,
        ).first()

        if not alert:
            return {"error": "Alert not found."}, 404

        data = request.get_json() or {}

        try:
            loaded = alert_schema.load(
                data,
                partial=True,
            )
        except ValidationError as error:
            return {"errors": error.messages}, 400

        allowed_fields = {
            "status",
            "assigned_to_user_id",
        }

        unexpected_fields = set(loaded) - allowed_fields

        if unexpected_fields:
            return {
                "error": "Only alert status and assignment can be changed.",
                "fields": sorted(unexpected_fields),
            }, 400

        if "assigned_to_user_id" in loaded:
            if not _has_capability(
                application,
                user.id,
                "alert.assign",
            ):
                return {"error": "Alert assignment capability is required."}, 403

            if not _valid_assignee(
                application,
                loaded["assigned_to_user_id"],
            ):
                return {"error": "Assigned user cannot access this application alert."}, 400

        if "status" in loaded:
            status = loaded["status"]

            status_capabilities = {
                "acknowledged": "alert.acknowledge",
                "investigating": "alert.investigate",
                "resolved": "alert.resolve",
                "dismissed": "alert.resolve",
            }

            capability = status_capabilities.get(status)

            if not capability:
                if status == "open" and alert.status != "open":
                    return {"error": "Reopening resolved or dismissed alerts is not supported yet."}, 400

                if status != alert.status:
                    return {"error": "Unsupported alert status transition."}, 400
            elif not _has_capability(
                application,
                user.id,
                capability,
            ):
                return {
                    "error": f"{capability} capability is required."
                }, 403

            now = datetime.now(timezone.utc)

            if status == "acknowledged" and not alert.acknowledged_at:
                alert.acknowledged_at = now

            if status in {"resolved", "dismissed"} and not alert.resolved_at:
                alert.resolved_at = now

            alert.status = status

        if "assigned_to_user_id" in loaded:
            alert.assigned_to_user_id = loaded["assigned_to_user_id"]

        db.session.commit()

        return alert_schema.dump(alert), 200
