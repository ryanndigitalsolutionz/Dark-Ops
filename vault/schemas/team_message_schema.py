from marshmallow import Schema, fields, validate


class TeamMessageSchema(Schema):
    id = fields.Str(dump_only=True)
    team_id = fields.Str(dump_only=True)
    sender_user_id = fields.Str(dump_only=True)
    reply_to_message_id = fields.Str(allow_none=True)
    content = fields.Str(required=True, validate=validate.Length(min=1, max=5000))
    created_at = fields.DateTime(dump_only=True)
    edited_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)


team_message_schema = TeamMessageSchema()
team_messages_schema = TeamMessageSchema(many=True)
