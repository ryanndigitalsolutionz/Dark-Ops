from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Regexp(r"^[a-z0-9_]+$"))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8, max=24))
    phone_number = fields.Str(required=True)
    first_name = fields.Str(required=True)
    surname = fields.Str(required=True)
    last_name = fields.Str(required=True)
    display_name = fields.Str(required=True)
    security_question = fields.Str(required=True)
    security_answer = fields.Str(required=True, load_only=True)
    turnstile_token = fields.Str(required=True, load_only=True)

class LoginSchema(Schema):
    login = fields.Str(required=True, load_only=True)
    password = fields.Str(required=True, load_only=True)
    turnstile_token = fields.Str(required=True, load_only=True)

class AuthenticationResponseSchema(Schema):
    success = fields.Bool()
    message = fields.Str()
    access_token = fields.Str()
    user = fields.Dict()

register_schema = RegisterSchema()
login_schema = LoginSchema()
authentication_response_schema = AuthenticationResponseSchema()
