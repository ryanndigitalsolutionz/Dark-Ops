from flask import Flask
from flask_restful import Api

from config import Config
from extensions import (
    bcrypt,
    cors,
    db,
    jwt,
    limiter,
    migrate,
    socketio,
)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ---------------------------------------------------------------
    # Extensions
    # ---------------------------------------------------------------

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, supports_credentials=True)
    jwt.init_app(app)
    limiter.init_app(app)

    socketio_kwargs = {}
    redis_url = (
        app.config.get("SOCKETIO_MESSAGE_QUEUE")
        or app.config.get("REDIS_URL")
    )

    if redis_url:
        socketio_kwargs["message_queue"] = redis_url

    socketio.init_app(app, **socketio_kwargs)

    # ---------------------------------------------------------------
    # Import models so SQLAlchemy metadata knows every table.
    # ---------------------------------------------------------------

    from models import (
        api_key,
        application,
        asset,
        audit_log,
        event,
        incident,
        incident_action,
        incident_note,
        mfa_factor,
        notification,
        profile,
        profile_completion,
        recovery_code,
        recovery_operation,
        response_connector,
        response_decision,
        response_policy,
        session,
        settings,
        subscription,
        subscription_application,
        team,
        team_api_key_request,
        team_api_key_vote,
        team_invitation,
        team_member,
        team_message,
        team_notification_rule,
        team_owner,
        team_role,
        usage_meter,
        user,
        vulnerability,
    )

    # ---------------------------------------------------------------
    # REST API
    # ---------------------------------------------------------------

    api = Api(app, prefix="/api")

    # ---------------------------------------------------------------
    # Authentication
    # ---------------------------------------------------------------

    from resources.authentication_resource import AuthenticationResource
    from resources.google_authentication_resource import (
        GoogleAuthenticationResource,
    )
    from resources.microsoft_authentication_resource import (
        MicrosoftAuthenticationResource,
    )
    from resources.mfa_factor_resource import MfaFactorResource

    api.add_resource(
        AuthenticationResource,
        "/authentication",
    )

    api.add_resource(
        GoogleAuthenticationResource,
        "/authentication/google",
    )

    api.add_resource(
        MicrosoftAuthenticationResource,
        "/authentication/microsoft",
    )

    api.add_resource(
        MfaFactorResource,
        "/mfa-factors",
        "/mfa-factors/<string:factor_id>",
    )

    # ---------------------------------------------------------------
    # User / Profile / Settings
    # ---------------------------------------------------------------

    from resources.user_resource import UserResource
    from resources.profile_resource import ProfileResource
    from resources.setting_resource import SettingResource

    api.add_resource(
        UserResource,
        "/users/me",
    )

    api.add_resource(
        ProfileResource,
        "/profile",
    )

    api.add_resource(
        SettingResource,
        "/settings",
    )

    # ---------------------------------------------------------------
    # Teams
    # ---------------------------------------------------------------

    from resources.team_resource import TeamResource
    from resources.team_owner_resource import TeamOwnerResource
    from resources.team_member_resource import TeamMemberResource
    from resources.team_role_resource import TeamRoleResource
    from resources.team_invitation_resource import TeamInvitationResource
    from resources.team_message_resource import TeamMessageResource
    from resources.team_notification_rule_resource import (
        TeamNotificationRuleResource,
    )
    from resources.team_api_key_request_resource import (
        TeamApiKeyRequestResource,
    )

    api.add_resource(
        TeamResource,
        "/teams",
        "/teams/<string:team_id>",
    )

    api.add_resource(
        TeamOwnerResource,
        "/teams/<string:team_id>/owner",
        "/teams/<string:team_id>/owner/<string:owner_id>",
    )

    api.add_resource(
        TeamMemberResource,
        "/teams/<string:team_id>/members",
        "/teams/<string:team_id>/members/<string:member_id>",
    )

    api.add_resource(
        TeamRoleResource,
        "/teams/<string:team_id>/roles",
        "/teams/<string:team_id>/roles/<string:role_id>",
    )

    api.add_resource(
        TeamInvitationResource,
        "/teams/<string:team_id>/invitations",
        "/teams/<string:team_id>/invitations/<string:invitation_id>",
    )

    api.add_resource(
        TeamMessageResource,
        "/teams/<string:team_id>/messages",
        "/teams/<string:team_id>/messages/<string:message_id>",
    )

    api.add_resource(
        TeamNotificationRuleResource,
        "/teams/<string:team_id>/notification-rules",
        "/teams/<string:team_id>/notification-rules/<string:rule_id>",
    )

    api.add_resource(
        TeamApiKeyRequestResource,
        "/teams/<string:team_id>/api-key-requests",
        "/teams/<string:team_id>/api-key-requests/<string:request_id>",
    )

    # ---------------------------------------------------------------
    # Applications / Assets
    # ---------------------------------------------------------------

    from resources.application_resource import ApplicationResource
    from resources.asset_resource import AssetResource

    api.add_resource(
        ApplicationResource,
        "/applications",
        "/applications/<string:application_id>",
    )

    api.add_resource(
        AssetResource,
        "/applications/<string:application_id>/assets",
        "/applications/<string:application_id>/assets/<string:asset_id>",
    )

    # ---------------------------------------------------------------
    # Detection → Alert → Incident → Vulnerability → Audit
    # ---------------------------------------------------------------

    from resources.event_resource import EventResource
    from resources.alert_resource import AlertResource
    from resources.incident_resource import IncidentResource
    from resources.incident_note_resource import IncidentNoteResource
    from resources.incident_action_resource import IncidentActionResource
    from resources.vulnerability_resource import VulnerabilityResource
    from resources.audit_log_resource import (
        AuditLogListResource,
        AuditLogResource,
    )

    api.add_resource(
        EventResource,
        "/applications/<string:application_id>/events",
        "/applications/<string:application_id>/events/<string:event_id>",
    )

    api.add_resource(
        AlertResource,
        "/applications/<string:application_id>/alerts",
        "/applications/<string:application_id>/alerts/<string:alert_id>",
    )

    api.add_resource(
        IncidentResource,
        "/applications/<string:application_id>/incidents",
        "/applications/<string:application_id>/incidents/<string:incident_id>",
    )

    api.add_resource(
        IncidentNoteResource,
        "/incidents/<string:incident_id>/notes",
        "/incidents/<string:incident_id>/notes/<string:note_id>",
    )

    api.add_resource(
        IncidentActionResource,
        "/incidents/<string:incident_id>/actions",
        "/incidents/<string:incident_id>/actions/<string:action_id>",
    )

    api.add_resource(
        VulnerabilityResource,
        "/applications/<string:application_id>/vulnerabilities",
        "/applications/<string:application_id>/vulnerabilities/<string:vulnerability_id>",
    )

    api.add_resource(
        AuditLogListResource,
        "/audit-logs",
    )

    api.add_resource(
        AuditLogResource,
        "/audit-logs/<string:log_id>",
    )

    # ---------------------------------------------------------------
    # Response / Recovery
    # ---------------------------------------------------------------

    from resources.response_resource import ResponseResource
    from resources.response_policy_resource import ResponsePolicyResource
    from resources.response_connector_resource import (
        ResponseConnectorResource,
    )
    from resources.recovery_resource import RecoveryResource

    api.add_resource(
        ResponseResource,
        "/incidents/<string:incident_id>/response",
        "/incidents/<string:incident_id>/response/<string:decision_id>",
    )

    api.add_resource(
        ResponsePolicyResource,
        "/response-policies",
        "/teams/<string:team_id>/response-policies",
        "/teams/<string:team_id>/response-policies/<string:policy_id>",
    )

    api.add_resource(
        ResponseConnectorResource,
        "/response-connectors",
        "/teams/<string:team_id>/response-connectors",
        "/teams/<string:team_id>/response-connectors/<string:connector_id>",
    )

    api.add_resource(
        RecoveryResource,
        "/incidents/<string:incident_id>/recovery",
        "/incidents/<string:incident_id>/recovery/<string:recovery_id>",
    )

    # ---------------------------------------------------------------
    # Notifications
    # ---------------------------------------------------------------

    from resources.notification_resource import NotificationResource

    api.add_resource(
        NotificationResource,
        "/notifications",
        "/notifications/<string:notification_id>",
    )

    # ---------------------------------------------------------------
    # API Keys / Subscriptions
    # ---------------------------------------------------------------

    from resources.api_key_resource import ApiKeyResource
    from resources.subscription_resource import SubscriptionResource

    api.add_resource(
        ApiKeyResource,
        "/api-keys",
        "/api-keys/<string:api_key_id>",
    )

    api.add_resource(
        SubscriptionResource,
        "/subscriptions",
        "/subscriptions/<string:subscription_id>",
    )

    # ---------------------------------------------------------------
    # Health
    # ---------------------------------------------------------------

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "service": "DarkOps",
        }, 200

    return app


app = create_app()


if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=app.config.get("DEBUG", False),
    )
