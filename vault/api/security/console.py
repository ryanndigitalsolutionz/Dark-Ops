CAPABILITIES = {
    # Team management
    "team.view": {
        "label": "View Team",
        "description": "View team information and membership.",
        "group": "team",
    },
    "team.view_members": {
        "label": "View Members",
        "description": "View team member information.",
        "group": "team",
    },
    "team.manage_members": {
        "label": "Manage Members",
        "description": "Manage team membership and member assignments.",
        "group": "team",
    },
    "team.view_presence": {
        "label": "View Member Presence",
        "description": "View member availability and last-seen status.",
        "group": "team",
    },
    "team.manage_member_access": {
        "label": "Manage Member Access",
        "description": "Manage a member's access to the team and its permitted resources.",
        "group": "team",
    },
    "team.manage_access_schedule": {
        "label": "Manage Access Schedule",
        "description": "Set temporary access schedules for team members.",
        "group": "team",
    },
    "team.assign_capabilities": {
        "label": "Assign Capabilities",
        "description": "Assign available capabilities to team members.",
        "group": "team",
    },
    "team.manage_notification_rules": {
        "label": "Manage Notification Rules",
        "description": "Configure which members receive selected team and security notifications.",
        "group": "team",
    },
    "team.send_broadcast": {
        "label": "Send Team Broadcast",
        "description": "Send an in-app broadcast to the permitted team audience.",
        "group": "team",
    },
    "team.manage_communication": {
        "label": "Manage Communication Settings",
        "description": "Configure the team's default communication channel.",
        "group": "team",
    },

    # Team Envelope
    "team_envelope.access": {
        "label": "Access Team Envelope",
        "description": "Access the team's group communication space.",
        "group": "communication",
    },
    "team_envelope.send": {
        "label": "Send Team Envelope Messages",
        "description": "Send messages through Team Envelope.",
        "group": "communication",
    },
    "team_envelope.select_recipients": {
        "label": "Select Message Recipients",
        "description": "Send a message to selected team members instead of the default team audience.",
        "group": "communication",
    },
    "team_envelope.view_targeting_trail": {
        "label": "View Targeting Trail",
        "description": "View the sender-to-recipient trail of explicitly targeted messages without message contents.",
        "group": "communication",
    },
    "team_envelope.archive_targeting_trail": {
        "label": "Archive Targeting Trail",
        "description": "Archive retained recipient-targeting trail history.",
        "group": "communication",
    },
    "team_envelope.manage": {
        "label": "Manage Team Envelope",
        "description": "Manage permitted Team Envelope settings.",
        "group": "communication",
    },

    # Live meetings
    "live_meeting.access": {
        "label": "Access Live Meetings",
        "description": "Participate in permitted live meetings.",
        "group": "communication",
    },
    "live_meeting.schedule": {
        "label": "Schedule Live Meetings",
        "description": "Schedule permitted team live meetings.",
        "group": "communication",
    },
    "live_meeting.manage": {
        "label": "Manage Live Meetings",
        "description": "Manage permitted team live-meeting settings and scheduling.",
        "group": "communication",
    },

    # In-app notifications
    "notification.receive": {
        "label": "Receive Notifications",
        "description": "Receive permitted in-app notifications.",
        "group": "notifications",
    },
    "notification.send": {
        "label": "Send Notifications",
        "description": "Send permitted in-app notifications to selected recipients.",
        "group": "notifications",
    },

    # Customer support
    "support.helpline": {
        "label": "Contact Admin Helpline",
        "description": "Contact DarkOps customer support through the admin helpline.",
        "group": "support",
    },
    "support.live_meeting_request": {
        "label": "Request Support Meeting",
        "description": "Request a live customer-support meeting with DarkOps administrators.",
        "group": "support",
    },

    # Protected applications
    "application.view": {
        "label": "View Applications",
        "description": "View permitted protected applications.",
        "group": "application",
    },
    "application.view_status": {
        "label": "View Application Wellbeing",
        "description": "View the security state and wellbeing of a protected application.",
        "group": "application",
    },
    "application.manage": {
        "label": "Manage Applications",
        "description": "Manage permitted protected application configuration.",
        "group": "application",
    },
    "application.configure_protection": {
        "label": "Configure Protection",
        "description": "Configure the protection settings of a permitted application.",
        "group": "application",
    },
    "application.connect": {
        "label": "Connect Applications",
        "description": "Connect an application to DarkOps protection.",
        "group": "application",
    },
    "application.disconnect": {
        "label": "Disconnect Applications",
        "description": "Disconnect a protected application from DarkOps protection.",
        "group": "application",
    },

    # Assets
    "asset.view": {
        "label": "View Assets",
        "description": "View assets associated with protected applications.",
        "group": "assets",
    },
    "asset.create": {
        "label": "Upload Assets",
        "description": "Upload or add permitted application security assets.",
        "group": "assets",
    },
    "asset.update": {
        "label": "Update Assets",
        "description": "Update permitted application security assets.",
        "group": "assets",
    },

    # Security events
    "event.view": {
        "label": "View Security Events",
        "description": "View retained security-relevant events.",
        "group": "security",
    },
    "event.inspect": {
        "label": "Inspect Security Events",
        "description": "Inspect evidence associated with retained security events.",
        "group": "security",
    },

    # Alerts
    "alert.view": {
        "label": "View Alerts",
        "description": "View permitted application alerts.",
        "group": "security",
    },
    "alert.create": {
        "label": "Create Alerts",
        "description": "Create authorized administrative alerts.",
        "group": "security",
    },
    "alert.acknowledge": {
        "label": "Acknowledge Alerts",
        "description": "Acknowledge permitted alerts.",
        "group": "security",
    },
    "alert.investigate": {
        "label": "Investigate Alerts",
        "description": "Investigate permitted alerts.",
        "group": "security",
    },
    "alert.assign": {
        "label": "Assign Alerts",
        "description": "Assign permitted alerts to eligible members.",
        "group": "security",
    },
    "alert.resolve": {
        "label": "Resolve Alerts",
        "description": "Resolve or dismiss permitted alerts.",
        "group": "security",
    },

    # Incidents
    "incident.view": {
        "label": "View Incidents",
        "description": "View permitted application incidents.",
        "group": "incidents",
    },
    "incident.manage": {
        "label": "Manage Incidents",
        "description": "Manage permitted application incidents.",
        "group": "incidents",
    },
    "incident.add_note": {
        "label": "Add Incident Notes",
        "description": "Add notes to permitted incidents.",
        "group": "incidents",
    },

    # Vulnerabilities
    "vulnerability.view": {
        "label": "View Vulnerabilities",
        "description": "View vulnerability assessments.",
        "group": "vulnerability",
    },
    "vulnerability.assess": {
        "label": "Assess Vulnerabilities",
        "description": "Perform permitted vulnerability assessments.",
        "group": "vulnerability",
    },

    # Response
    "response.view": {
        "label": "View Responses",
        "description": "View response decisions and response activity.",
        "group": "response",
    },
    "response.review": {
        "label": "Review Responses",
        "description": "Review proposed response decisions.",
        "group": "response",
    },
    "response.approve": {
        "label": "Approve Responses",
        "description": "Approve response decisions requiring authorization.",
        "group": "response",
    },
    "response.execute": {
        "label": "Execute Responses",
        "description": "Execute authorized response actions.",
        "group": "response",
    },
    "response_policy.view": {
        "label": "View Response Policies",
        "description": "View permitted application response policies.",
        "group": "response",
    },
    "response_policy.manage": {
        "label": "Manage Response Policies",
        "description": "Create, update and disable permitted response policies.",
        "group": "response",
    },
    "response_connector.view": {
        "label": "View Response Connectors",
        "description": "View permitted response connectors.",
        "group": "response",
    },
    "response_connector.manage": {
        "label": "Manage Response Connectors",
        "description": "Create, update and disable permitted response connectors.",
        "group": "response",
    },

    # Recovery
    "recovery.view": {
        "label": "View Recovery",
        "description": "View recovery operations and verification results.",
        "group": "recovery",
    },
    "recovery.initiate": {
        "label": "Initiate Recovery",
        "description": "Initiate authorized recovery operations.",
        "group": "recovery",
    },
    "recovery.verify": {
        "label": "Verify Recovery",
        "description": "Verify whether recovery restored the application's security state.",
        "group": "recovery",
    },

    # Audit
    "audit.view": {
        "label": "View Audit Log",
        "description": "View permitted audit activity.",
        "group": "audit",
    },
    "audit.view_team": {
        "label": "View Team Audit Trail",
        "description": "View audit activity associated with team operations.",
        "group": "audit",
    },
    "audit.view_application": {
        "label": "View Application Audit Trail",
        "description": "View audit activity associated with a protected application.",
        "group": "audit",
    },
}


DEFAULT_MEMBER_CAPABILITIES = {
    "team_envelope.access",
    "team_envelope.send",
    "notification.receive",
    "support.helpline",
}


def get_capabilities():
    return CAPABILITIES.copy()


def get_capability(key):
    return CAPABILITIES.get(key)


def capability_exists(key):
    return key in CAPABILITIES


def get_capabilities_by_group(group):
    return {
        key: value for key, value in CAPABILITIES.items()
        if value["group"] == group
    }


def get_default_member_capabilities():
    return set(DEFAULT_MEMBER_CAPABILITIES)
