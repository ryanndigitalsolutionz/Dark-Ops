import uuid
from datetime import datetime, timezone
from extensions import db


class SubscriptionApplication(db.Model):
    __tablename__ = "subscription_application"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    subscription_id = db.Column(db.String(36), db.ForeignKey("subscription.id"), nullable=False, index=True)
    application_id = db.Column(db.String(36), db.ForeignKey("application.id"), nullable=False, index=True)
    status = db.Column(db.String(30), nullable=False, default="active", index=True)
    attached_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    detached_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    subscription = db.relationship("Subscription", back_populates="subscription_applications")
    application = db.relationship("Application", back_populates="subscription_applications")

    __table_args__ = (
        db.UniqueConstraint("subscription_id", "application_id", name="uq_subscription_application"),
    )
