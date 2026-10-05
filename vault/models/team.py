import uuid
from datetime import datetime, timezone
from extensions import db


class Team(db.Model):
    __tablename__ = "team"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    team_id = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    team_display_name = db.Column(
        db.String(150),
        nullable=False,
    )

    slug = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    description = db.Column(db.Text)

    status = db.Column(
        db.String(30),
        nullable=False,
        default="active",
        index=True,
    )

    live_access_status = db.Column(
        db.String(30),
        nullable=False,
        default="locked",
        index=True,
    )

    live_access_granted_at = db.Column(
        db.DateTime(timezone=True),
    )

    created_by_user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.id"),
        nullable=False,
        index=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    terminated_at = db.Column(
        db.DateTime(timezone=True),
    )

    created_by_user = db.relationship(
        "User",
        foreign_keys=[created_by_user_id],
        back_populates="created_teams",
    )

    team_owners = db.relationship(
        "TeamOwner",
        back_populates="team",
        cascade="all, delete-orphan",
    )

    members = db.relationship(
        "TeamMember",
        back_populates="team",
        cascade="all, delete-orphan",
    )

    roles = db.relationship(
        "TeamRole",
        back_populates="team",
        cascade="all, delete-orphan",
    )

    invitations = db.relationship(
        "TeamInvitation",
        back_populates="team",
        cascade="all, delete-orphan",
    )

    messages = db.relationship(
        "TeamMessage",
        back_populates="team",
        cascade="all, delete-orphan",
    )

    applications = db.relationship(
        "Application",
        back_populates="team",
    )

    notification_rules = db.relationship(
        "TeamNotificationRule",
        back_populates="team",
        cascade="all, delete-orphan",
    )

    response_policies = db.relationship(
        "ResponsePolicy",
        back_populates="team",
        cascade="all, delete-orphan",
    )

    response_connectors = db.relationship(
        "ResponseConnector",
        back_populates="team",
        cascade="all, delete-orphan",
    )

    subscriptions = db.relationship(
        "Subscription",
        back_populates="team",
    )

    api_keys = db.relationship(
        "ApiKey",
        back_populates="team",
    )

    usage_meters = db.relationship(
        "UsageMeter",
        back_populates="team",
    )

    audit_logs = db.relationship(
        "AuditLog",
        back_populates="team",
    )

    notifications = db.relationship(
        "Notification",
        back_populates="team",
    )
