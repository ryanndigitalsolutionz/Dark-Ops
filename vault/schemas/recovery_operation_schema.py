from marshmallow import Schema, fields, validate


class RecoveryOperationSchema(Schema):
    id = fields.Str(dump_only=True)

    incident_id = fields.Str(dump_only=True)

    initiated_by_user_id = fields.Str(
        dump_only=True,
        allow_none=True,
    )

    actor_type = fields.Str(
        dump_only=True,
        validate=validate.OneOf([
            "darkops",
            "user",
            "system",
        ]),
    )

    operation_type = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=150),
    )

    target = fields.Str(allow_none=True)

    status = fields.Str(
        dump_only=True,
        validate=validate.OneOf([
            "pending",
            "running",
            "succeeded",
            "failed",
            "verified",
            "rejected",
        ]),
    )

    parameters = fields.Dict(allow_none=True)

    result = fields.Dict(
        dump_only=True,
        allow_none=True,
    )

    verification_metadata = fields.Dict(
        dump_only=True,
        allow_none=True,
    )

    created_at = fields.DateTime(dump_only=True)
    started_at = fields.DateTime(dump_only=True, allow_none=True)
    completed_at = fields.DateTime(dump_only=True, allow_none=True)
    verified_at = fields.DateTime(dump_only=True, allow_none=True)


recovery_operation_schema = RecoveryOperationSchema()
recovery_operations_schema = RecoveryOperationSchema(many=True)
