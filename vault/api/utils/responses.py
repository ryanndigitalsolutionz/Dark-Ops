from flask import jsonify


def success(data=None, message=None, status_code=200):
    payload = {
        "success": True,
    }

    if message is not None:
        payload["message"] = message

    if data is not None:
        payload["data"] = data

    return jsonify(payload), status_code


def error(
    message,
    status_code=400,
    code=None,
    details=None,
):
    payload = {
        "success": False,
        "error": {
            "message": message,
        },
    }

    if code is not None:
        payload["error"]["code"] = code

    if details is not None:
        payload["error"]["details"] = details

    return jsonify(payload), status_code
