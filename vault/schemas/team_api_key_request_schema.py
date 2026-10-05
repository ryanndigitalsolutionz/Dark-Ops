from marshmallow import Schema, fields, validate


class TeamApiKeyRequestSchema(Schema):
    id = fields.String(dump_only=True)
    request_id = fields.String(dump_only=True)

    team_id = fields.String(dump_only=True)
    application_id = fields.String(required=True)
    subscription_id = fields.String(required=True)

    requested_by_user_id = fields.String(dump_only=True)
    reviewed_by_user_id = fields.String(dump_only=True, allow_none=True)

    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=150),
    )
    mode = fields.String(
        required=True,
        validate=validate.OneOf(["build", "protection"]),
    )
    environment = fields.String(
        required=True,
        validate=validate.OneOf(["test", "live"]),
    )
    reason = fields.String(
        allow_none=True,
        validate=validate.Length(max=5000),
    )

    status = fields.String(dump_only=True)

    vote_threshold = fields.Decimal(
        as_string=True,
        dump_only=True,
    )
    total_vote_percentage = fields.Decimal(
        as_string=True,
        dump_only=True,
    )
    vote_count = fields.Integer(dump_only=True)

    owner_decision = fields.String(
        dump_only=True,
        allow_none=True,
    )
    owner_decided_at = fields.DateTime(
        dump_only=True,
        allow_none=True,
    )

    api_key_id = fields.String(
        dump_only=True,
        allow_none=True,
    )

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    expires_at = fields.DateTime(dump_only=True, allow_none=True)
    completed_at = fields.DateTime(dump_only=True, allow_none=True)
