from marshmallow import Schema, fields, validate


class SettingSchema(Schema):
    id = fields.String(dump_only=True)
    user_id = fields.String(dump_only=True)
    profile_id = fields.String(dump_only=True, allow_none=True)
    theme = fields.String(validate=validate.OneOf(["dark", "light"]))
    timezone = fields.String(allow_none=True, validate=validate.Length(max=100))
    default_environment = fields.String(
        validate=validate.OneOf(["test", "live"])
    )
    email_notifications = fields.Boolean()
    security_notifications = fields.Boolean()
    announcement_notifications = fields.Boolean()
    privacy_preferences = fields.Dict(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
