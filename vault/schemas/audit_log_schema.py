from marshmallow import Schema, fields, validate


class AuditLogSchema(Schema):
    id = fields.Str(dump_only=True)

    team_id = fields.Str(
        dump_only=True,
        allow_none=True
    )

    actor_user_id = fields.Str(
        dump_only=True,
        allow_none=True
    )

    application_id = fields.Str(
        dump_only=True,
        allow_none=True
    )

    api_key_id = fields.Str(
        dump_only=True,
        allow_none=True
    )

    subscription_id = fields.Str(
        dump_only=True,
        allow_none=True
    )

    asset_id = fields.Str(
        dump_only=True,
        allow_none=True
    )

    event_id = fields.Str(
        dump_only=True,
        allow_none=True
    )

    alert_id = fields.Str(
        dump_only=True,
        allow_none=True
    )

    incident_id = fields.Str(
        dump_only=True,
        allow_none=True
    )

    access_method = fields.Str(
        dump_only=True,
        validate=validate.OneOf(["api", "console"])
    )

    action = fields.Str(
        dump_only=True,
        validate=validate.Length(min=1, max=150)
    )

    resource_type = fields.Str(
        dump_only=True,
        validate=validate.Length(min=1, max=100)
    )

    resource_id = fields.Str(
        dump_only=True,
        allow_none=True
    )

    ip_address = fields.Str(
        dump_only=True,
        allow_none=True
    )

    user_agent = fields.Str(
        dump_only=True,
        allow_none=True
    )

    metadata = fields.Dict(
        dump_only=True,
        allow_none=True
    )

    occurred_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


audit_log_schema = AuditLogSchema()
audit_logs_schema = AuditLogSchema(many=True)
