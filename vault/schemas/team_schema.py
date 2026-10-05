from marshmallow import Schema, fields, validate


class TeamSchema(Schema):
    id = fields.Str(dump_only=True)
    team_id = fields.Str(dump_only=True)
    owner_user_id = fields.Str(dump_only=True)
    team_display_name = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    slug = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    description = fields.Str(allow_none=True, validate=validate.Length(max=2000))
    status = fields.Str(dump_only=True)
    live_access_status = fields.Str(dump_only=True)
    live_access_granted_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    terminated_at = fields.DateTime(dump_only=True)


team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)
