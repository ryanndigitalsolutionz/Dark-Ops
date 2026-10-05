from marshmallow import Schema, fields, validate


class TeamNotificationRuleSchema(Schema):
    id = fields.Str(dump_only=True)
    team_id = fields.Str(dump_only=True)
    application_id = fields.Str(allow_none=True)
    created_by_user_id = fields.Str(dump_only=True)
    target_user_id = fields.Str(required=True)
    minimum_severity = fields.Str(allow_none=True, validate=validate.OneOf(["informational", "low", "medium", "high", "critical"]))
    event_types = fields.List(
        fields.Str(validate=validate.Length(min=1, max=150)), allow_none=True
    )
    notification_channels = fields.List(
        fields.Str(validate=validate.OneOf(["in_app", "email", "sms", "webhook"])), allow_none=True
    )
    enabled = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


team_notification_rule_schema = TeamNotificationRuleSchema()
team_notification_rules_schema = TeamNotificationRuleSchema(many=True)
