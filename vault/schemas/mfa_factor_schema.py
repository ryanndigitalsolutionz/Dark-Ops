from marshmallow import Schema, fields, validate


class MfaFactorSchema(Schema):
    id = fields.String(dump_only=True)
    user_id = fields.String(dump_only=True)
    type = fields.String(
        required=True,
        validate=validate.OneOf([
            "totp",
            "sms",
            "email",
            "webauthn",
        ]),
    )
    name = fields.String(
        allow_none=True,
        validate=validate.Length(max=100),
    )
    is_primary = fields.Boolean()
    is_verified = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    verified_at = fields.DateTime(dump_only=True, allow_none=True)
    last_used_at = fields.DateTime(dump_only=True, allow_none=True)
