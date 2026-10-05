from marshmallow import Schema, fields, validate


class TeamInvitationSchema(Schema):
    id = fields.Str(dump_only=True)
    team_id = fields.Str(dump_only=True)
    role_id = fields.Str(required=True)
    invited_by_user_id = fields.Str(dump_only=True)
    accepted_user_id = fields.Str(dump_only=True)
    email = fields.Email(required=True)
    status = fields.Str(dump_only=True)
    expires_at = fields.DateTime(dump_only=True)
    invited_at = fields.DateTime(dump_only=True)
    accepted_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


team_invitation_schema = TeamInvitationSchema()
team_invitations_schema = TeamInvitationSchema(many=True)
