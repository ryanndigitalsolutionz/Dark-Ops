import uuid
from datetime import datetime, timezone

from extensions import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    u1_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(320), unique=True, nullable=False, index=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    phone_number = db.Column(db.String(30), unique=True)
    phone_verified_at = db.Column(db.DateTime(timezone=True))
    password_hash = db.Column(db.Text)
    google_subject = db.Column(db.String(255), unique=True)
    microsoft_subject = db.Column(db.String(255), unique=True)
    status = db.Column(db.String(30), nullable=False, default="active", index=True)
    email_verified_at = db.Column(db.DateTime(timezone=True))
    security_question = db.Column(db.Text)
    security_answer_hash = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_login_at = db.Column(db.DateTime(timezone=True))

    profile = db.relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    profile_completion = db.relationship("ProfileCompletion", back_populates="user", uselist=False, cascade="all, delete-orphan")
    settings = db.relationship("Settings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sessions = db.relationship("Session", back_populates="user", cascade="all, delete-orphan")
    mfa_factors = db.relationship("MfaFactor", back_populates="user", cascade="all, delete-orphan")
    recovery_codes = db.relationship("RecoveryCode", back_populates="user", cascade="all, delete-orphan")

    team_memberships = db.relationship("TeamMember", back_populates="user", cascade="all, delete-orphan")
    created_teams = db.relationship("Team", foreign_keys="Team.created_by_user_id", back_populates="created_by_user")
    team_ownerships = db.relationship("TeamOwner", foreign_keys="TeamOwner.user_id", back_populates="user")
    assigned_team_owners = db.relationship("TeamOwner", foreign_keys="TeamOwner.assigned_by_user_id", back_populates="assigned_by_user")
    sent_team_invitations = db.relationship("TeamInvitation", foreign_keys="TeamInvitation.invited_by_user_id", back_populates="invited_by")
    accepted_team_invitations = db.relationship("TeamInvitation", foreign_keys="TeamInvitation.accepted_user_id", back_populates="accepted_user")
    sent_team_messages = db.relationship("TeamMessage", back_populates="sender")

    owned_applications = db.relationship("Application", foreign_keys="Application.owner_user_id", back_populates="owner")
    created_applications = db.relationship("Application", foreign_keys="Application.created_by_user_id", back_populates="created_by")

    owned_api_keys = db.relationship("ApiKey", foreign_keys="ApiKey.owner_user_id", back_populates="owner_user")
    created_api_keys = db.relationship("ApiKey", foreign_keys="ApiKey.created_by_user_id", back_populates="created_by_user")

    owned_subscriptions = db.relationship("Subscription", foreign_keys="Subscription.owner_user_id", back_populates="owner_user")
    created_subscriptions = db.relationship("Subscription", foreign_keys="Subscription.created_by_user_id", back_populates="created_by_user")

    usage_meters = db.relationship("UsageMeter", back_populates="owner_user")
    notifications = db.relationship("Notification", foreign_keys="Notification.user_id", back_populates="user")
    sent_notifications = db.relationship("Notification", foreign_keys="Notification.sender_user_id", back_populates="sender")

    incident_notes = db.relationship("IncidentNote", back_populates="author")
    incident_actions = db.relationship("IncidentAction", back_populates="triggered_by")
    audit_logs = db.relationship("AuditLog", back_populates="actor_user")

    created_notification_rules = db.relationship("TeamNotificationRule", foreign_keys="TeamNotificationRule.created_by_user_id", back_populates="created_by_user")
    notification_targets = db.relationship("TeamNotificationRule", foreign_keys="TeamNotificationRule.target_user_id", back_populates="target_user")

    created_response_policies = db.relationship("ResponsePolicy", back_populates="created_by_user")
    response_decisions = db.relationship("ResponseDecision", foreign_keys="ResponseDecision.decided_by_user_id", back_populates="decided_by_user")
    approved_response_decisions = db.relationship("ResponseDecision", foreign_keys="ResponseDecision.approved_by_user_id", back_populates="approved_by_user")
    created_response_connectors = db.relationship("ResponseConnector", back_populates="created_by_user")
    initiated_recovery_operations = db.relationship("RecoveryOperation", back_populates="initiated_by_user")
