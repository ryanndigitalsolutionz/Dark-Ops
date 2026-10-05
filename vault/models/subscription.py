import uuid
from datetime import datetime, timezone
from extensions import db


class Subscription(db.Model):
    __tablename__ = "subscription"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), nullable=True, index=True)
    created_by_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    plan_code = db.Column(db.String(50), nullable=False, index=True)
    plan_name = db.Column(db.String(100), nullable=False)
    access_method = db.Column(db.String(30), nullable=False)
    benefits = db.Column(db.JSON)
    limits = db.Column(db.JSON)
    amount = db.Column(db.Numeric(20, 6), nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="EUR")
    billing_interval = db.Column(db.String(30), nullable=False, default="quarterly")
    status = db.Column(db.String(30), nullable=False, index=True)
    auto_renew = db.Column(db.Boolean, nullable=False, default=True)
    cancel_at_period_end = db.Column(db.Boolean, nullable=False, default=False)
    provider = db.Column(db.String(50))
    provider_customer_reference = db.Column(db.String(255))
    provider_subscription_reference = db.Column(db.String(255), index=True)
    latest_payment_reference = db.Column(db.String(255))
    started_at = db.Column(db.DateTime(timezone=True))
    next_billing_at = db.Column(db.DateTime(timezone=True), index=True)
    expires_at = db.Column(db.DateTime(timezone=True), index=True)
    cancelled_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner_user = db.relationship("User", foreign_keys=[owner_user_id], back_populates="owned_subscriptions")
    team = db.relationship("Team", back_populates="subscriptions")
    created_by_user = db.relationship("User", foreign_keys=[created_by_user_id], back_populates="created_subscriptions")
    subscription_applications = db.relationship("SubscriptionApplication", back_populates="subscription")
    api_keys = db.relationship("ApiKey", back_populates="subscription")
    usage_meters = db.relationship("UsageMeter", back_populates="subscription")
    audit_logs = db.relationship("AuditLog", back_populates="subscription")
