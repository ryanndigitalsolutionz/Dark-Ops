from marshmallow import Schema, fields, validate


class ResponsePolicySchema(Schema):
    id = fields.Str(dump_only=True)

    owner_user_id = fields.Str(dump_only=True, allow_none=True)
    team_id = fields.Str(dump_only=True, allow_none=True)
    created_by_user_id = fields.Str(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=150),
    )

    description = fields.Str(
        allow_none=True,
        validate=validate.Length(max=5000),
    )

    execution_mode = fields.Str(
        validate=validate.OneOf([
            "approval_required",
            "automatic",
        ])
    )

    triggers = fields.Dict(allow_none=True)
    rules = fields.Dict(allow_none=True)

    enabled = fields.Bool(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


response_policy_schema = ResponsePolicySchema()
response_policies_schema = ResponsePolicySchema(many=True)
