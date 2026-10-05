import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.team_invitation import TeamInvitation
from models.team_member import TeamMember
from models.team_role import TeamRole
from models.user import User
from schemas.team_invitation_schema import TeamInvitationSchema


invitation_schema = TeamInvitationSchema()
invitations_schema = TeamInvitationSchema(many=True)


def _member(team_id, user_id):
    return TeamMember.query.filter_by(
        team_id=team_id,
        user_id=user_id,
        status="active",
    ).first()


class TeamInvitationResource(Resource):
    @jwt_required()
    def get(self, team_id, invitation_id=None):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        if invitation_id:
            invitation = TeamInvitation.query.filter_by(
                id=invitation_id,
                team_id=team_id,
            ).first()

            if not invitation:
                return {"error": "Invitation not found."}, 404

            return invitation_schema.dump(invitation), 200

        invitations = (
            TeamInvitation.query
            .filter_by(team_id=team_id)
            .order_by(TeamInvitation.created_at.desc())
            .all()
        )

        return {"items": invitations_schema.dump(invitations)}, 200

    @jwt_required()
    def post(self, team_id):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        data = request.get_json() or {}

        try:
            loaded = invitation_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        role = TeamRole.query.filter_by(
            id=loaded["role_id"],
            team_id=team_id,
        ).first()

        if not role:
            return {"error": "Role does not belong to this team."}, 400

        email = loaded["email"].strip().lower()
        existing_member = (
            TeamMember.query
            .join(User)
            .filter(
                TeamMember.team_id == team_id,
                User.email == email,
                TeamMember.status == "active",
            )
            .first()
        )

        if existing_member:
            return {"error": "That user is already a team member."}, 409

        pending = TeamInvitation.query.filter_by(
            team_id=team_id,
            email=email,
            status="pending",
        ).first()

        if pending:
            return {"error": "A pending invitation already exists for that email."}, 409

        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        invitation = TeamInvitation(
            team_id=team_id,
            role_id=role.id,
            invited_by_user_id=user_id,
            email=email,
            token_hash=token_hash,
            status="pending",
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
            invited_at=datetime.now(timezone.utc),
        )

        db.session.add(invitation)
        db.session.commit()

        response = invitation_schema.dump(invitation)
        response["invitation_token"] = raw_token

        return response, 201

    @jwt_required()
    def delete(self, team_id, invitation_id):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        invitation = TeamInvitation.query.filter_by(
            id=invitation_id,
            team_id=team_id,
        ).first()

        if not invitation:
            return {"error": "Invitation not found."}, 404

        invitation.status = "revoked"
        db.session.commit()

        return {"message": "Invitation revoked successfully."}, 200

    def accept(self):
        data = request.get_json() or {}
        token = data.get("token")

        if not token:
            return {"error": "Invitation token is required."}, 400

        token_hash = hashlib.sha256(token.encode()).hexdigest()

        invitation = TeamInvitation.query.filter_by(
            token_hash=token_hash,
            status="pending",
        ).first()

        if not invitation:
            return {"error": "Invalid or unavailable invitation."}, 404

        if invitation.expires_at and invitation.expires_at < datetime.now(timezone.utc):
            invitation.status = "expired"
            db.session.commit()
            return {"error": "Invitation has expired."}, 410

        user_id = get_jwt_identity() if request.headers.get("Authorization") else None

        if not user_id:
            return {"error": "Authentication required."}, 401

        user = db.session.get(User, user_id)

        if not user or user.email.lower() != invitation.email.lower():
            return {"error": "The authenticated account does not match the invitation."}, 403

        existing = TeamMember.query.filter_by(
            team_id=invitation.team_id,
            user_id=user.id,
        ).first()

        if existing:
            existing.status = "active"
            existing.role_id = invitation.role_id
            invitation.accepted_user_id = user.id
            invitation.status = "accepted"
            invitation.accepted_at = datetime.now(timezone.utc)
            db.session.commit()
            return {"message": "Invitation accepted successfully."}, 200

        member = TeamMember(
            team_id=invitation.team_id,
            user_id=user.id,
            role_id=invitation.role_id,
            status="active",
            joined_at=datetime.now(timezone.utc),
        )

        invitation.accepted_user_id = user.id
        invitation.status = "accepted"
        invitation.accepted_at = datetime.now(timezone.utc)

        db.session.add(member)
        db.session.commit()

        return {"message": "Invitation accepted successfully."}, 200
