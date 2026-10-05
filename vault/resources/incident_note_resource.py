from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.incident import Incident
from models.incident_note import IncidentNote
from models.team_member import TeamMember
from schemas.incident_note_schema import IncidentNoteSchema


note_schema = IncidentNoteSchema()
notes_schema = IncidentNoteSchema(many=True)


def _can_access(incident, user_id):
    application = incident.application

    if application.owner_user_id == user_id:
        return True

    if application.team_id:
        return bool(
            TeamMember.query.filter_by(
                team_id=application.team_id,
                user_id=user_id,
                status="active",
            ).first()
        )

    return False


class IncidentNoteResource(Resource):
    @jwt_required()
    def get(self, incident_id, note_id=None):
        user_id = get_jwt_identity()
        incident = db.session.get(Incident, incident_id)

        if not incident or not _can_access(incident, user_id):
            return {"error": "Incident not found or access denied."}, 404

        if note_id:
            note = IncidentNote.query.filter_by(
                id=note_id,
                incident_id=incident_id,
            ).first()

            if not note:
                return {"error": "Incident note not found."}, 404

            return note_schema.dump(note), 200

        notes = (
            IncidentNote.query
            .filter_by(incident_id=incident_id)
            .order_by(IncidentNote.created_at.asc())
            .all()
        )

        return {"items": notes_schema.dump(notes)}, 200

    @jwt_required()
    def post(self, incident_id):
        user_id = get_jwt_identity()
        incident = db.session.get(Incident, incident_id)

        if not incident or not _can_access(incident, user_id):
            return {"error": "Incident not found or access denied."}, 404

        data = request.get_json() or {}

        try:
            loaded = note_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        note = IncidentNote(
            incident_id=incident_id,
            author_user_id=user_id,
            content=loaded["content"],
        )

        db.session.add(note)
        db.session.commit()

        return note_schema.dump(note), 201

    @jwt_required()
    def patch(self, incident_id, note_id):
        user_id = get_jwt_identity()
        note = IncidentNote.query.filter_by(
            id=note_id,
            incident_id=incident_id,
        ).first()

        if not note:
            return {"error": "Incident note not found."}, 404

        if note.author_user_id != user_id:
            return {"error": "Only the note author can edit this note."}, 403

        data = request.get_json() or {}

        try:
            loaded = note_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        if "content" in loaded:
            note.content = loaded["content"]

        db.session.commit()

        return note_schema.dump(note), 200

    @jwt_required()
    def delete(self, incident_id, note_id):
        user_id = get_jwt_identity()
        note = IncidentNote.query.filter_by(
            id=note_id,
            incident_id=incident_id,
        ).first()

        if not note:
            return {"error": "Incident note not found."}, 404

        if note.author_user_id != user_id:
            return {"error": "Only the note author can delete this note."}, 403

        db.session.delete(note)
        db.session.commit()

        return {"message": "Incident note deleted successfully."}, 200
