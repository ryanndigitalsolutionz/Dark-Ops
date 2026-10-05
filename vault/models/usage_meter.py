import uuid
from datetime import datetime, timezone
from extensions import db


class UsageMeter(db.Model):
    __tablename__ = "usage_meter"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False, index=True)
    team_id = db.Column(db.String(36), db.ForeignKey("team.id"), nullable=True, index=True)
    subscription_id = db.Column(db.String(36), db.ForeignKey("subscription.id"), nullable=False, index=True)
    application_id = db.Column(db.String(36), db.ForeignKey("application.id"), nullable=True, index=True)
    api_key_id = db.Column(db.String(36), db.ForeignKey("api_key.id"), nullable=True, index=True)
    credit_type = db.Column(db.String(30), nullable=False, index=True)
    metric = db.Column(db.String(100), nullable=False, index=True)
    unit = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Numeric(20, 6), nullable=False)
    severity = db.Column(db.String(30), index=True)
    asset_type = db.Column(db.String(50), index=True)
    http_method = db.Column(db.String(10))
    access_method = db.Column(db.String(20))
    mode = db.Column(db.String(20))
    environment = db.Column(db.String(20), index=True)
    credits_consumed = db.Column(db.Numeric(20, 6), nullable=False, default=0)
    measured_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), index=True)
    period_start = db.Column(db.DateTime(timezone=True), index=True)
    period_end = db.Column(db.DateTime(timezone=True), index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner_user = db.relationship("User", back_populates="usage_meters")
    team = db.relationship("Team", back_populates="usage_meters")
    subscription = db.relationship("Subscription", back_populates="usage_meters")
    application = db.relationship("Application", back_populates="usage_meters")
    api_key = db.relationship("ApiKey", back_populates="usage_meters")

    __table_args__ = (
        db.Index("ix_usage_meter_subscription_period", "subscription_id", "period_start", "period_end"),
        db.Index("ix_usage_meter_owner_measured", "owner_user_id", "measured_at"),
    )
