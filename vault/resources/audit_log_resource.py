from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from api.authentication.authentication import get_current_user
from models.audit_log import AuditLog
from models.team import Team
from models.team_member import TeamMember
from models.application import Application
from schemas.audit_log_schema import audit_log_schema, audit_logs_schema


def get_accessible_audit_logs(user):
    return (
        AuditLog.query
        .outerjoin(
            Application,
            AuditLog.application_id == Application.id
        )
        .outerjoin(
            Team,
            AuditLog.team_id == Team.id
        )
        .outerjoin(
            TeamMember,
            AuditLog.team_id == TeamMember.team_id
        )
        .filter(
            or_(
                Application.owner_user_id == user.id,
                Team.owner_user_id == user.id,
                TeamMember.user_id == user.id
            )
        )
        .distinct()
        .order_by(AuditLog.occurred_at.desc())
        .all()
    )


def get_accessible_audit_log(log_id, user):
    return (
        AuditLog.query
        .outerjoin(
            Application,
            AuditLog.application_id == Application.id
        )
        .outerjoin(
            Team,
            AuditLog.team_id == Team.id
        )
        .outerjoin(
            TeamMember,
            AuditLog.team_id == TeamMember.team_id
        )
        .filter(
            AuditLog.id == log_id,
            or_(
                Application.owner_user_id == user.id,
                Team.owner_user_id == user.id,
                TeamMember.user_id == user.id
            )
        )
        .first()
    )


class AuditLogListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            user = get_current_user()
            audit_logs = get_accessible_audit_logs(user)

            return {
                "success": True,
                "audit_logs": audit_logs_schema.dump(audit_logs)
            }, 200

        except ValueError as error:
            return {
                "success": False,
                "message": str(error)
            }, 401

        except SQLAlchemyError:
            return {
                "success": False,
                "message": "Unable to retrieve audit logs."
            }, 500


class AuditLogResource(Resource):
    @jwt_required()
    def get(self, log_id):
        try:
            user = get_current_user()

            audit_log = get_accessible_audit_log(
                log_id,
                user
            )

            if not audit_log:
                return {
                    "success": False,
                    "message": "Audit log not found."
                }, 404

            return {
                "success": True,
                "audit_log": audit_log_schema.dump(audit_log)
            }, 200

        except ValueError as error:
            return {
                "success": False,
                "message": str(error)
            }, 401

        except SQLAlchemyError:
            return {
                "success": False,
                "message": "Unable to retrieve the audit log."
            }, 500
