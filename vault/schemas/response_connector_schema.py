from marshmallow import Schema, fields, validate


class ResponseConnectorSchema(Schema):
    id = fields.Str(dump_only=True)

    owner_user_id = fields.Str(dump_only=True, allow_none=True)
    team_id = fields.Str(dump_only=True, allow_none=True)
    created_by_user_id = fields.Str(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=150),
    )

    type = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
    )

    base_url = fields.Str(allow_none=True)

    configuration = fields.Dict(
        load_only=True,
        allow_none=True,
    )

    status = fields.Str(
        dump_only=True,
        validate=validate.OneOf([
            "active",
            "inactive",
            "revoked",
            "error",
        ]),
    )

    metadata = fields.Dict(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


response_connector_schema = ResponseConnectorSchema()
response_connectors_schema = ResponseConnectorSchema(many=True)
