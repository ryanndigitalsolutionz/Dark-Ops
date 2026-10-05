from marshmallow import Schema, fields, validate


class IncidentActionSchema(Schema):
    id = fields.Str(dump_only=True)
    incident_id = fields.Str(dump_only=True)
    triggered_by_user_id = fields.Str(dump_only=True, allow_none=True)
    action_type = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    target = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.Length(min=1, max=30))
    parameters = fields.Dict(allow_none=True)
    result = fields.Dict(allow_none=True)
    error_message = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    started_at = fields.DateTime(dump_only=True)
    completed_at = fields.DateTime(dump_only=True)


incident_action_schema = IncidentActionSchema()
incident_actions_schema = IncidentActionSchema(many=True)