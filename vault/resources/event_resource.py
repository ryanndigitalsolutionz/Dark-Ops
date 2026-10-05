from flask_restful import Resource

from extensions import db
from models.application import Application
from models.event import Event
from schemas.event_schema import EventSchema

from api.authentication.authentication import get_current_user


event_schema = EventSchema()
events_schema = EventSchema(many=True)


def _can_access_application(application, user):
    if not application or not user:
        return False

    if application.owner_user_id == user.id:
        return True

    if application.team_id:
        from models.team_member import TeamMember

        return bool(
            TeamMember.query.filter_by(
                team_id=application.team_id,
                user_id=user.id,
                status="active",
            ).first()
        )

    return False


class EventResource(Resource):
    def get(self, application_id, event_id=None):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        application = db.session.get(
            Application,
            application_id,
        )

        if not application or not _can_access_application(
            application,
            user,
        ):
            return {
                "error": "Application not found or access denied."
            }, 404

        if event_id:
            event = Event.query.filter_by(
                id=event_id,
                application_id=application_id,
            ).first()

            if not event:
                return {"error": "Event not found."}, 404

            return event_schema.dump(event), 200

        events = (
            Event.query
            .filter_by(application_id=application_id)
            .order_by(Event.occurred_at.desc())
            .all()
        )

        return {
            "items": events_schema.dump(events)
        }, 200
