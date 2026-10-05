from marshmallow import Schema, fields, validate


class TeamRoleSchema(Schema):
    id = fields.Str(dump_only=True)
    team_id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(allow_none=True, validate=validate.Length(max=1000))
    is_system_role = fields.Bool(dump_only=True)
    permissions = fields.Dict(allow_none=True)
    console_layout = fields.Dict(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


team_role_schema = TeamRoleSchema()
team_roles_schema = TeamRoleSchema(many=True)
