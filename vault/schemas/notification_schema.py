from marshmallow import Schema, fields, validate


NOTIFICATION_TYPES = [
    "security_alert",
    "event",
    "incident",
    "vulnerability",
    "payment",
    "announcement",
    "system",
    "team",
    "authentication",
]


class NotificationSchema(Schema):
    id = fields.Str(dump_only=True)

    user_id = fields.Str(dump_only=True)
    team_id = fields.Str(dump_only=True, allow_none=True)
    sender_user_id = fields.Str(dump_only=True, allow_none=True)

    event_id = fields.Str(dump_only=True, allow_none=True)
    alert_id = fields.Str(dump_only=True, allow_none=True)
    incident_id = fields.Str(dump_only=True, allow_none=True)
    vulnerability_id = fields.Str(dump_only=True, allow_none=True)

    type = fields.Str(
        dump_only=True,
        validate=validate.OneOf(NOTIFICATION_TYPES),
    )

    status = fields.Str(
        dump_only=True,
        validate=validate.OneOf([
            "unread",
            "read",
        ]),
    )

    title = fields.Str(
        dump_only=True,
    )

    message = fields.Str(
        dump_only=True,
    )

    sound_key = fields.Str(
        dump_only=True,
        allow_none=True,
    )

    action_key = fields.Str(
        dump_only=True,
        allow_none=True,
    )

    action_url = fields.Url(
        dump_only=True,
        allow_none=True,
    )

    metadata = fields.Dict(
        dump_only=True,
        allow_none=True,
    )

    created_at = fields.DateTime(
        dump_only=True,
    )

    read_at = fields.DateTime(
        dump_only=True,
        allow_none=True,
    )


notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)
