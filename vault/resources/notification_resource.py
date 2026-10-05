from datetime import datetime, timezone

from flask_restful import Resource

from api.authentication.authentication import get_current_user
from extensions import db
from models.notification import Notification
from schemas.notification_schema import NotificationSchema


notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)


class NotificationResource(Resource):
    def get(self, notification_id=None):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        if notification_id:
            notification = Notification.query.filter_by(
                id=notification_id,
                user_id=user.id,
            ).first()

            if not notification:
                return {"error": "Notification not found."}, 404

            return notification_schema.dump(notification), 200

        notifications = (
            Notification.query
            .filter_by(user_id=user.id)
            .order_by(Notification.created_at.desc())
            .all()
        )

        return {
            "items": notifications_schema.dump(notifications)
        }, 200

    def patch(self, notification_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user.id,
        ).first()

        if not notification:
            return {"error": "Notification not found."}, 404

        notification.status = "read"

        if not notification.read_at:
            notification.read_at = datetime.now(timezone.utc)

        db.session.commit()

        return notification_schema.dump(notification), 200

    def delete(self, notification_id):
        user = get_current_user()

        if not user:
            return {"error": "Authentication required."}, 401

        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user.id,
        ).first()

        if not notification:
            return {"error": "Notification not found."}, 404

        db.session.delete(notification)
        db.session.commit()

        return {
            "message": "Notification deleted successfully."
        }, 200
