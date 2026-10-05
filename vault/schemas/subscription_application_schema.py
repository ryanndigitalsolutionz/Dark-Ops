from marshmallow import Schema, fields, validate


class SubscriptionApplicationSchema(Schema):
    id = fields.Str(dump_only=True)

    subscription_id = fields.Str(
        required=True
    )

    application_id = fields.Str(
        required=True
    )

    status = fields.Str(
        dump_only=True,
        validate=validate.Length(min=1, max=30)
    )

    attached_at = fields.DateTime(dump_only=True)
    detached_at = fields.DateTime(dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


subscription_application_schema = SubscriptionApplicationSchema()
subscription_applications_schema = SubscriptionApplicationSchema(many=True)
