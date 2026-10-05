from marshmallow import Schema, fields, validate


class SubscriptionCheckoutSchema(Schema):
    plan_code = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )
    team_id = fields.String(
        allow_none=True,
    )
    success_url = fields.Url(
        required=False,
        allow_none=True,
    )
    cancel_url = fields.Url(
        required=False,
        allow_none=True,
    )
