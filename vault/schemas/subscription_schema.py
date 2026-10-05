from marshmallow import Schema, fields, validate


class SubscriptionSchema(Schema):
    id = fields.Str(dump_only=True)

    owner_user_id = fields.Str(dump_only=True)
    team_id = fields.Str(dump_only=True, allow_none=True)
    created_by_user_id = fields.Str(dump_only=True)

    plan_code = fields.Str(
        dump_only=True,
        validate=validate.Length(min=1, max=50)
    )

    plan_name = fields.Str(
        dump_only=True,
        validate=validate.Length(min=1, max=100)
    )

    access_method = fields.Str(
        dump_only=True,
        validate=validate.Length(min=1, max=30)
    )

    benefits = fields.Dict(
        dump_only=True,
        allow_none=True
    )

    limits = fields.Dict(
        dump_only=True,
        allow_none=True
    )

    amount = fields.Decimal(
        dump_only=True,
        as_string=False
    )

    currency = fields.Str(
        dump_only=True,
        validate=validate.Length(equal=3)
    )

    billing_interval = fields.Str(
        dump_only=True,
        validate=validate.OneOf(["quarterly"])
    )

    status = fields.Str(
        dump_only=True,
        validate=validate.Length(min=1, max=30)
    )

    auto_renew = fields.Bool(dump_only=True)
    cancel_at_period_end = fields.Bool(dump_only=True)

    provider = fields.Str(
        dump_only=True,
        allow_none=True,
        validate=validate.Length(max=50)
    )

    provider_customer_reference = fields.Str(
        dump_only=True,
        allow_none=True,
        validate=validate.Length(max=255)
    )

    provider_subscription_reference = fields.Str(
        dump_only=True,
        allow_none=True,
        validate=validate.Length(max=255)
    )

    latest_payment_reference = fields.Str(
        dump_only=True,
        allow_none=True,
        validate=validate.Length(max=255)
    )

    started_at = fields.DateTime(dump_only=True, allow_none=True)
    next_billing_at = fields.DateTime(dump_only=True, allow_none=True)
    expires_at = fields.DateTime(dump_only=True, allow_none=True)
    cancelled_at = fields.DateTime(dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


subscription_schema = SubscriptionSchema()
subscriptions_schema = SubscriptionSchema(many=True)
