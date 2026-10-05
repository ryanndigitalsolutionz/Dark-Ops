from marshmallow import Schema, fields, validate


class AssetSchema(Schema):
    id = fields.Str(dump_only=True)
    application_id = fields.Str(dump_only=True)

    name = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    identifier = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    type = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    status = fields.Str(dump_only=True)
    description = fields.Str(allow_none=True, validate=validate.Length(max=2000))

    original_filename = fields.Str(dump_only=True)
    mime_type = fields.Str(dump_only=True)
    size_bytes = fields.Integer(dump_only=True)
    storage_provider = fields.Str(dump_only=True)
    storage_key = fields.Str(dump_only=True)
    checksum_sha256 = fields.Str(dump_only=True)

    analysis_status = fields.Str(dump_only=True)
    analysis_metadata = fields.Dict(dump_only=True, allow_none=True)
    last_analyzed_at = fields.DateTime(dump_only=True)

    metadata = fields.Dict(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


asset_schema = AssetSchema()
assets_schema = AssetSchema(many=True)
