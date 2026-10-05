from marshmallow import Schema, fields, validate


EVENT_SEVERITIES = [
    "informational",
    "low",
    "medium",
    "high",
    "critical",
]

EVENT_VERIFICATION_MODES = [
    "passive",
    "authenticated",
    "authorized_active",
    "external_tool",
]

EVENT_ORIGINS = [
    "darkops",
    "user",
    "system",
    "external",
]


class EventSchema(Schema):
    id = fields.Str(dump_only=True)

    application_id = fields.Str(dump_only=True)
    asset_id = fields.Str(dump_only=True, allow_none=True)

    source = fields.Str(
        dump_only=True,
    )

    category = fields.Str(
        dump_only=True,
        allow_none=True,
    )

    event_type = fields.Str(
        dump_only=True,
    )

    detection_check = fields.Str(
        dump_only=True,
        allow_none=True,
    )

    verification_mode = fields.Str(
        dump_only=True,
        validate=validate.OneOf(EVENT_VERIFICATION_MODES),
    )

    origin = fields.Str(
        dump_only=True,
        validate=validate.OneOf(EVENT_ORIGINS),
    )

    severity = fields.Str(
        dump_only=True,
        validate=validate.OneOf(EVENT_SEVERITIES),
    )

    confidence = fields.Decimal(
        dump_only=True,
        as_string=False,
        allow_none=True,
    )

    fingerprint = fields.Str(
        dump_only=True,
        allow_none=True,
    )

    title = fields.Str(
        dump_only=True,
        allow_none=True,
    )

    description = fields.Str(
        dump_only=True,
        allow_none=True,
    )

    actor_identifier = fields.Str(
        dump_only=True,
        allow_none=True,
    )

    payload = fields.Dict(
        dump_only=True,
        allow_none=True,
    )

    occurred_at = fields.DateTime(dump_only=True)
    received_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


event_schema = EventSchema()
events_schema = EventSchema(many=True)
