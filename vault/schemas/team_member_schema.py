from marshmallow import Schema, fields, validate


class TeamMemberSchema(Schema):
    id = fields.Str(dump_only=True)
    team_id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)
    role_id = fields.Str(required=True)
    status = fields.Str(dump_only=True)
    joined_at = fields.DateTime(dump_only=True)
    suspended_at = fields.DateTime(dump_only=True)
    left_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


team_member_schema = TeamMemberSchema()
team_members_schema = TeamMemberSchema(many=True)
