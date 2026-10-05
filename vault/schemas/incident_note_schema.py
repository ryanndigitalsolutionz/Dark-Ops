from marshmallow import Schema, fields, validate


class IncidentNoteSchema(Schema):
    id = fields.Str(dump_only=True)
    incident_id = fields.Str(dump_only=True)
    author_user_id = fields.Str(dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=1, max=10000))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


incident_note_schema = IncidentNoteSchema()
incident_notes_schema = IncidentNoteSchema(many=True)