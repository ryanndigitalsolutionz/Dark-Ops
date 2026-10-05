RINGTONES = {
    "access_blocked": {
        "path": "/assets/category/audio/system_notifications/mixkit-alarm-clock-beep-988.wav",
        "purpose": "Team member access has been temporarily blocked.",
    },
    "warning": {
        "path": "/assets/category/audio/system_notifications/mixkit-vintage-warning-alarm-990.wav",
        "purpose": "DarkOps has raised or held a security alert/incident that requires attention.",
    },
    "interface": {
        "path": "/assets/category/audio/system_notifications/mixkit-software-interface-back-2575.wav",
        "purpose": "Open or close the DarkOps extension or expand/collapse Customer Support.",
    },
    "success": {
        "path": "/assets/category/audio/system_notifications/mixkit-confirmation-tone-2867.wav",
        "purpose": "A requested operation or action completed successfully.",
    },
    "message": {
        "path": "/assets/category/audio/system_notifications/mixkit-long-pop-2358.wav",
        "purpose": "A new general or targeted message/notification appears for its recipient during active chat.",
    },
    "reminder": {
        "path": "/assets/category/audio/system_notifications/mixkit-interface-option-select-2573.wav",
        "purpose": "A reminder that unfinished or unsubmitted work is preventing a requested action.",
    },
}


def get_ringtone(sound_key):
    if not sound_key:
        raise ValueError("Ringtone key is required.")

    ringtone = RINGTONES.get(sound_key)

    if ringtone is None:
        raise ValueError(f"Unknown ringtone: {sound_key}")

    return ringtone


def ringtone_exists(sound_key):
    return sound_key in RINGTONES


def get_ringtones():
    return {
        key: dict(value)
        for key, value in RINGTONES.items()
    }
