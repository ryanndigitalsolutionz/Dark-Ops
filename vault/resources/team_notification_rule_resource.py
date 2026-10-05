from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.application import Application
from models.team_member import TeamMember
from models.team_notification_rule import TeamNotificationRule
from schemas.team_notification_rule_schema import TeamNotificationRuleSchema


rule_schema = TeamNotificationRuleSchema()
rules_schema = TeamNotificationRuleSchema(many=True)


def _member(team_id, user_id):
    return TeamMember.query.filter_by(
        team_id=team_id,
        user_id=user_id,
        status="active",
    ).first()


def _validate_target(team_id, target_user_id):
    if target_user_id is None:
        return True

    return bool(
        TeamMember.query.filter_by(
            team_id=team_id,
            user_id=target_user_id,
            status="active",
        ).first()
    )


def _validate_application(team_id, application_id):
    if application_id is None:
        return True

    return bool(
        Application.query.filter_by(
            id=application_id,
            team_id=team_id,
        ).first()
    )


class TeamNotificationRuleResource(Resource):
    @jwt_required()
    def get(self, team_id, rule_id=None):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        if rule_id:
            rule = TeamNotificationRule.query.filter_by(
                id=rule_id,
                team_id=team_id,
            ).first()

            if not rule:
                return {"error": "Notification rule not found."}, 404

            return rule_schema.dump(rule), 200

        rules = (
            TeamNotificationRule.query
            .filter_by(team_id=team_id)
            .order_by(TeamNotificationRule.created_at.desc())
            .all()
        )

        return {"items": rules_schema.dump(rules)}, 200

    @jwt_required()
    def post(self, team_id):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        data = request.get_json() or {}

        try:
            loaded = rule_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        if not _validate_target(team_id, loaded.get("target_user_id")):
            return {"error": "Target user must be an active team member."}, 400

        if not _validate_application(team_id, loaded.get("application_id")):
            return {"error": "Application does not belong to this team."}, 400

        rule = TeamNotificationRule(
            team_id=team_id,
            application_id=loaded.get("application_id"),
            created_by_user_id=user_id,
            target_user_id=loaded.get("target_user_id"),
            minimum_severity=loaded.get("minimum_severity"),
            event_types=loaded.get("event_types", []),
            notification_channels=loaded.get("notification_channels", []),
            enabled=loaded.get("enabled", True),
        )

        db.session.add(rule)
        db.session.commit()

        return rule_schema.dump(rule), 201

    @jwt_required()
    def patch(self, team_id, rule_id):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        rule = TeamNotificationRule.query.filter_by(
            id=rule_id,
            team_id=team_id,
        ).first()

        if not rule:
            return {"error": "Notification rule not found."}, 404

        data = request.get_json() or {}

        try:
            loaded = rule_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        if "target_user_id" in loaded and not _validate_target(team_id, loaded["target_user_id"]):
            return {"error": "Target user must be an active team member."}, 400

        if "application_id" in loaded and not _validate_application(team_id, loaded["application_id"]):
            return {"error": "Application does not belong to this team."}, 400

        for field, value in loaded.items():
            if field not in {"id", "team_id", "created_by_user_id"}:
                setattr(rule, field, value)

        db.session.commit()

        return rule_schema.dump(rule), 200

    @jwt_required()
    def delete(self, team_id, rule_id):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        rule = TeamNotificationRule.query.filter_by(
            id=rule_id,
            team_id=team_id,
        ).first()

        if not rule:
            return {"error": "Notification rule not found."}, 404

        db.session.delete(rule)
        db.session.commit()

        return {"message": "Notification rule deleted successfully."}, 200
