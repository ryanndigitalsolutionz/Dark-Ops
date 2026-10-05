from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models.subscription import Subscription
from models.team_member import TeamMember
from schemas.subscription_schema import SubscriptionSchema


subscription_schema = SubscriptionSchema()
subscriptions_schema = SubscriptionSchema(many=True)


def _can_access(subscription, user_id):
    if subscription.owner_user_id == user_id:
        return True

    if subscription.team_id:
        return bool(
            TeamMember.query.filter_by(
                team_id=subscription.team_id,
                user_id=user_id,
                status="active",
            ).first()
        )

    return False


class SubscriptionResource(Resource):
    @jwt_required()
    def get(self, subscription_id=None):
        user_id = get_jwt_identity()

        if subscription_id:
            subscription = db.session.get(Subscription, subscription_id)

            if not subscription or not _can_access(subscription, user_id):
                return {"error": "Subscription not found or access denied."}, 404

            return subscription_schema.dump(subscription), 200

        subscriptions = (
            Subscription.query
            .filter(
                (Subscription.owner_user_id == user_id)
                | Subscription.team_id.in_(
                    db.session.query(TeamMember.team_id).filter(
                        TeamMember.user_id == user_id,
                        TeamMember.status == "active",
                    )
                )
            )
            .order_by(Subscription.created_at.desc())
            .all()
        )

        return {"items": subscriptions_schema.dump(subscriptions)}, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json() or {}

        try:
            loaded = subscription_schema.load(data)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        team_id = loaded.get("team_id")

        if team_id:
            membership = TeamMember.query.filter_by(
                team_id=team_id,
                user_id=user_id,
                status="active",
            ).first()

            if not membership:
                return {"error": "You are not an active member of this team."}, 403

        subscription = Subscription(
            owner_user_id=user_id,
            team_id=team_id,
            created_by_user_id=user_id,
            plan_code=loaded["plan_code"],
            plan_name=loaded["plan_name"],
            access_method=loaded.get("access_method"),
            benefits=loaded.get("benefits"),
            limits=loaded.get("limits"),
            amount=loaded["amount"],
            currency="EUR",
            billing_interval="quarterly",
            status=loaded.get("status", "pending"),
            auto_renew=loaded.get("auto_renew", True),
            cancel_at_period_end=loaded.get("cancel_at_period_end", False),
            provider=loaded.get("provider"),
            provider_customer_id=loaded.get("provider_customer_id"),
            provider_subscription_id=loaded.get("provider_subscription_id"),
            started_at=loaded.get("started_at"),
            next_billing_at=loaded.get("next_billing_at"),
            expires_at=loaded.get("expires_at"),
            cancelled_at=loaded.get("cancelled_at"),
        )

        db.session.add(subscription)
        db.session.commit()

        return subscription_schema.dump(subscription), 201

    @jwt_required()
    def patch(self, subscription_id):
        user_id = get_jwt_identity()
        subscription = db.session.get(Subscription, subscription_id)

        if not subscription or not _can_access(subscription, user_id):
            return {"error": "Subscription not found or access denied."}, 404

        data = request.get_json() or {}

        try:
            loaded = subscription_schema.load(data, partial=True)
        except ValidationError as error:
            return {"errors": error.messages}, 400

        for field, value in loaded.items():
            if field not in {
                "id",
                "owner_user_id",
                "team_id",
                "created_by_user_id",
                "currency",
                "billing_interval",
                "provider_customer_id",
                "provider_subscription_id",
            }:
                setattr(subscription, field, value)

        db.session.commit()

        return subscription_schema.dump(subscription), 200
