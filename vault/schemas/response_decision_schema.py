from marshmallow import Schema, fields, validate


class ResponseDecisionSchema(Schema):
    id = fields.Str(dump_only=True)
    incident_id = fields.Str(dump_only=True)

    policy_id = fields.Str(allow_none=True)
    connector_id = fields.Str(allow_none=True)

    action_type = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=150),
    )

    execution_mode = fields.Str(
        dump_only=True,
        validate=validate.OneOf([
            "approval_required",
            "automatic",
        ]),
    )

    target_scope = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
    )

    target = fields.Str(allow_none=True)

    status = fields.Str(
        dump_only=True,
        validate=validate.OneOf([
            "pending",
            "approved",
            "rejected",
            "executing",
            "completed",
            "failed",
            "held",
        ]),
    )

    rationale = fields.Str(
        allow_none=True,
        validate=validate.Length(max=10000),
    )

    decided_by_user_id = fields.Str(
        dump_only=True,
        allow_none=True,
    )

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    approved_at = fields.DateTime(dump_only=True, allow_none=True)
    completed_at = fields.DateTime(dump_only=True, allow_none=True)


response_decision_schema = ResponseDecisionSchema()
response_decisions_schema = ResponseDecisionSchema(many=True)
