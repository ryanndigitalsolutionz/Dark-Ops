from marshmallow import Schema, fields, validate


class UsageMeterSchema(Schema):
    id = fields.Str(dump_only=True)

    owner_user_id = fields.Str(dump_only=True)
    team_id = fields.Str(dump_only=True, allow_none=True)
    subscription_id = fields.Str(dump_only=True)
    application_id = fields.Str(dump_only=True, allow_none=True)
    api_key_id = fields.Str(dump_only=True, allow_none=True)

    credit_type = fields.Str(
        required=True,
        validate=validate.OneOf(["workload", "duo_dev"])
    )

    metric = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    unit = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )

    quantity = fields.Decimal(
        required=True,
        as_string=False
    )

    severity = fields.Str(
        allow_none=True,
        validate=validate.OneOf([
            "informational",
            "low",
            "medium",
            "high",
            "critical"
        ])
    )

    asset_type = fields.Str(
        allow_none=True,
        validate=validate.Length(max=50)
    )

    http_method = fields.Str(
        allow_none=True,
        validate=validate.OneOf([
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "HEAD",
            "OPTIONS"
        ])
    )

    access_method = fields.Str(
        allow_none=True,
        validate=validate.OneOf(["api", "console"])
    )

    mode = fields.Str(
        allow_none=True,
        validate=validate.OneOf(["build", "protection"])
    )

    environment = fields.Str(
        allow_none=True,
        validate=validate.OneOf(["test", "live"])
    )

    credits_consumed = fields.Decimal(
        dump_only=True,
        as_string=False
    )

    measured_at = fields.DateTime(dump_only=True)
    period_start = fields.DateTime(allow_none=True)
    period_end = fields.DateTime(allow_none=True)

    metadata = fields.Dict(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


usage_meter_schema = UsageMeterSchema()
usage_meters_schema = UsageMeterSchema(many=True)
