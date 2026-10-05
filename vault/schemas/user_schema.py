from marshmallow import Schema, fields
from schemas.profile_schema import ProfileSchema


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    u1_id = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    username = fields.Str(dump_only=True)
    phone_number = fields.Str(dump_only=True)
    phone_verified_at = fields.DateTime(dump_only=True)
    status = fields.Str(dump_only=True)
    email_verified_at = fields.DateTime(dump_only=True)
    last_login_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    profile = fields.Nested(ProfileSchema, dump_only=True)
    profile_completion = fields.Dict(dump_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)