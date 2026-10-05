from marshmallow import Schema, fields, validate


class ApplicationSchema(Schema):
    id = fields.Str(dump_only=True)
    owner_user_id = fields.Str(dump_only=True, allow_none=True)
    team_id = fields.Str(dump_only=True, allow_none=True)
    created_by_user_id = fields.Str(dump_only=True)

    name = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    slug = fields.Str(dump_only=True)
    type = fields.Str(required=True, validate=validate.Length(min=1, max=50))

    environment = fields.Str(
        load_default="test",
        validate=validate.OneOf(["test", "live"]),
    )

    status = fields.Str(dump_only=True)

    authorized_primary_url = fields.Url(
        required=True,
        schemes={"https"},
    )

    base_url = fields.Url(
        allow_none=True,
        schemes={"https"},
    )

    description = fields.Str(
        allow_none=True,
        validate=validate.Length(max=2000),
    )

    detection_state = fields.Dict(dump_only=True)

    webhook_url = fields.Url(
        allow_none=True,
        schemes={"https"},
    )

    webhook_secret_hash = fields.Str(dump_only=True)
    webhook_secret_prefix = fields.Str(dump_only=True)
    webhook_active = fields.Bool(dump_only=True)

    webhook_events = fields.List(
        fields.Str(),
        allow_none=True,
    )

    webhook_last_delivery_at = fields.DateTime(dump_only=True)
    connected_at = fields.DateTime(dump_only=True)
    disconnected_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)
