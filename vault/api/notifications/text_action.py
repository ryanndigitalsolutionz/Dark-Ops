TEXT_ACTIONS = {
    "undo": {
        "label": "Undo",
        "description": "Undo the operation that just occurred.",
    },
    "view_application": {
        "label": "View Application",
        "description": "Open the related protected application.",
        "destination": "applications",
    },
    "view_asset": {
        "label": "View Asset",
        "description": "Open the related security asset.",
        "destination": "assets",
    },
    "view_event": {
        "label": "View Event",
        "description": "Open the related security event.",
        "destination": "events",
    },
    "view_alert": {
        "label": "View Alert",
        "description": "Open the related security alert.",
        "destination": "alerts",
    },
    "view_incident": {
        "label": "View Incident",
        "description": "Open the related security incident.",
        "destination": "incidents",
    },
    "view_vulnerability": {
        "label": "View Vulnerability",
        "description": "Open the related vulnerability.",
        "destination": "vulnerabilities",
    },
    "view_response": {
        "label": "View Response",
        "description": "Open the related response decision or action.",
        "destination": "response",
    },
    "view_recovery": {
        "label": "View Recovery",
        "description": "Open the related recovery operation.",
        "destination": "recovery",
    },
    "view_notifications": {
        "label": "View Notifications",
        "description": "Open the notification center.",
        "destination": "notifications",
    },
    "view_team": {
        "label": "View Team",
        "description": "Open the related team.",
        "destination": "teams",
    },
    "open_support": {
        "label": "Open Support",
        "description": "Open the Customer Support panel.",
    },
    "open_chat": {
        "label": "Open Chat",
        "description": "Open the related in-app conversation.",
    },
    "open_profile": {
        "label": "Open Profile",
        "description": "Open the related user profile.",
        "destination": "profile",
    },
    "dismiss": {
        "label": "Dismiss",
        "description": "Dismiss the current notification.",
    },
}


def get_text_action(action_key):
    if not action_key:
        raise ValueError("Text action key is required.")

    action = TEXT_ACTIONS.get(action_key)

    if action is None:
        raise ValueError(f"Unknown text action: {action_key}")

    return {
        "key": action_key,
        **action,
    }


def text_action_exists(action_key):
    return bool(action_key) and action_key in TEXT_ACTIONS


def get_text_actions():
    return {
        key: {
            "key": key,
            **value,
        }
        for key, value in TEXT_ACTIONS.items()
    }
