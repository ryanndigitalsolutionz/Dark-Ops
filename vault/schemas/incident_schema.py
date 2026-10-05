from marshmallow import Schema, fields, validate


INCIDENT_SEVERITIES = [
    "informational",
    "low",
    "medium",
    "high",
    "critical",
]

INCIDENT_STATUSES = [
    "open",
    "investigating",
    "contained",
    "resolved",
    "closed",
]


class IncidentSchema(Schema):
    id = fields.Str(dump_only=True)

    application_id = fields.Str(dump_only=True)

    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
    )

    description = fields.Str(
        allow_none=True,
    )

    severity = fields.Str(
        required=True,
        validate=validate.OneOf(INCIDENT_SEVERITIES),
    )

    status = fields.Str(
        validate=validate.OneOf(INCIDENT_STATUSES),
    )

    assigned_to_user_id = fields.Str(
        allow_none=True,
    )

    opened_at = fields.DateTime(
        dump_only=True,
    )

    contained_at = fields.DateTime(
        dump_only=True,
    )

    resolved_at = fields.DateTime(
        dump_only=True,
    )

    closed_at = fields.DateTime(
        dump_only=True,
    )

    resolution = fields.Str(
        allow_none=True,
    )

    metadata = fields.Dict(
        allow_none=True,
    )

    created_at = fields.DateTime(
        dump_only=True,
    )

    updated_at = fields.DateTime(
        dump_only=True,
    )


incident_schema = IncidentSchema()
incidents_schema = IncidentSchema(many=True)