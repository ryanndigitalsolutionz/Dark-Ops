from marshmallow import Schema, fields, validate


class ApiKeySchema(Schema):
    id = fields.Str(dump_only=True)

    owner_user_id = fields.Str(dump_only=True)
    team_id = fields.Str(dump_only=True, allow_none=True)

    application_id = fields.Str(
        required=True
    )

    subscription_id = fields.Str(
        required=True
    )

    created_by_user_id = fields.Str(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=150)
    )

    mode = fields.Str(
        required=True,
        validate=validate.OneOf(["build", "protection"])
    )

    environment = fields.Str(
        required=True,
        validate=validate.OneOf(["test", "live"])
    )

    public_key = fields.Str(dump_only=True)

    secret_key_prefix = fields.Str(dump_only=True)

    public_scopes = fields.Dict(
        allow_none=True
    )

    secret_scopes = fields.Dict(
        allow_none=True
    )

    status = fields.Str(
        dump_only=True,
        validate=validate.Length(min=1, max=30)
    )

    created_at = fields.DateTime(dump_only=True)
    expires_at = fields.DateTime(dump_only=True, allow_none=True)
    last_used_at = fields.DateTime(dump_only=True, allow_none=True)
    rotated_at = fields.DateTime(dump_only=True, allow_none=True)
    revoked_at = fields.DateTime(dump_only=True, allow_none=True)
    updated_at = fields.DateTime(dump_only=True)


api_key_schema = ApiKeySchema()
api_keys_schema = ApiKeySchema(many=True)
