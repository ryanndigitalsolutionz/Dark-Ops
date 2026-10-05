from marshmallow import Schema, fields, validate


class TeamOwnerSchema(Schema):
    id = fields.Str(dump_only=True)
    team_id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    assigned_by_user_id = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True, validate=validate.OneOf(["active", "removed"]))
    assigned_at = fields.DateTime(dump_only=True)
    removed_at = fields.DateTime(dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


team_owner_schema = TeamOwnerSchema()
team_owners_schema = TeamOwnerSchema(many=True)
