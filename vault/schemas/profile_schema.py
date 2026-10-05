from marshmallow import Schema, fields, validate


class ProfileSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(dump_only=True)

    first_name = fields.Str(
        allow_none=True,
        validate=validate.Length(max=100),
    )

    last_name = fields.Str(
        allow_none=True,
        validate=validate.Length(max=100),
    )

    display_name = fields.Str(
        allow_none=True,
        validate=validate.Length(max=150),
    )

    avatar_url = fields.Url(
        allow_none=True,
    )

    bio = fields.Str(
        allow_none=True,
        validate=validate.Length(max=1000),
    )

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)
