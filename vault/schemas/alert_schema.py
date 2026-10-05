from marshmallow import Schema, fields, validate


class AlertSchema(Schema):
    id = fields.Str(dump_only=True)
    application_id = fields.Str(dump_only=True)

    asset_id = fields.Str(allow_none=True)
    event_id = fields.Str(allow_none=True)
    incident_id = fields.Str(allow_none=True)

    created_by_user_id = fields.Str(dump_only=True)
    origin = fields.Str(dump_only=True)

    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
    )

    description = fields.Str(allow_none=True)

    alert_type = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=150),
    )

    severity = fields.Str(
        required=True,
        validate=validate.OneOf([
            "informational",
            "low",
            "medium",
            "high",
            "critical",
        ]),
    )

    status = fields.Str(
        dump_only=True,
    )

    assigned_to_user_id = fields.Str(allow_none=True)

    first_seen_at = fields.DateTime(dump_only=True)
    last_seen_at = fields.DateTime(dump_only=True)
    acknowledged_at = fields.DateTime(dump_only=True)
    resolved_at = fields.DateTime(dump_only=True)

    metadata = fields.Dict(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


alert_schema = AlertSchema()
alerts_schema = AlertSchema(many=True)
