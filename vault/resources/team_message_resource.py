from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.team_message import TeamMessage
from models.team_member import TeamMember
from schemas.team_message_schema import TeamMessageSchema


message_schema = TeamMessageSchema()
messages_schema = TeamMessageSchema(many=True)


def _member(team_id, user_id):
    return TeamMember.query.filter_by(
        team_id=team_id,
        user_id=user_id,
        status="active",
    ).first()


class TeamMessageResource(Resource):
    @jwt_required()
    def get(self, team_id, message_id=None):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        if message_id:
            message = TeamMessage.query.filter_by(
                id=message_id,
                team_id=team_id,
            ).first()

            if not message:
                return {"error": "Message not found."}, 404

            return message_schema.dump(message), 200

        messages = (
            TeamMessage.query
            .filter_by(team_id=team_id)
            .order_by(TeamMessage.created_at.asc())
            .all()
        )

        return {"items": messages_schema.dump(messages)}, 200

    @jwt_required()
    def post(self, team_id):
        user_id = get_jwt_identity()

        if not _member(team_id, user_id):
            return {"error": "Team access denied."}, 403

        data = request.get_json() or {}

        try:
            loaded = message_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        reply_to_message_id = loaded.get("reply_to_message_id")

        if reply_to_message_id:
            reply = TeamMessage.query.filter_by(
                id=reply_to_message_id,
                team_id=team_id,
            ).first()

            if not reply:
                return {"error": "Reply target not found in this team."}, 400

        message = TeamMessage(
            team_id=team_id,
            sender_user_id=user_id,
            content=loaded["content"],
            reply_to_message_id=reply_to_message_id,
        )

        db.session.add(message)
        db.session.commit()

        return message_schema.dump(message), 201

    @jwt_required()
    def patch(self, team_id, message_id):
        user_id = get_jwt_identity()

        message = TeamMessage.query.filter_by(
            id=message_id,
            team_id=team_id,
        ).first()

        if not message:
            return {"error": "Message not found."}, 404

        if message.sender_user_id != user_id:
            return {"error": "Only the message sender can edit this message."}, 403

        data = request.get_json() or {}

        try:
            loaded = message_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        if "content" in loaded:
            message.content = loaded["content"]
            message.is_edited = True

        db.session.commit()

        return message_schema.dump(message), 200

    @jwt_required()
    def delete(self, team_id, message_id):
        user_id = get_jwt_identity()

        message = TeamMessage.query.filter_by(
            id=message_id,
            team_id=team_id,
        ).first()

        if not message:
            return {"error": "Message not found."}, 404

        if message.sender_user_id != user_id:
            return {"error": "Only the message sender can delete this message."}, 403

        db.session.delete(message)
        db.session.commit()

        return {"message": "Message deleted successfully."}, 200
