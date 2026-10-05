import re
import secrets
import string


USER_ID_PREFIX = "UR_"
USER_ID_LENGTH = 5

TEAM_ID_MIN_LENGTH = 5
TEAM_ID_MAX_LENGTH = 9

TEAM_ID_ALPHABET = string.ascii_letters + string.digits
USER_ID_ALPHABET = string.ascii_lowercase + string.digits


def generate_user_id():
    value = "".join(
        secrets.choice(USER_ID_ALPHABET)
        for _ in range(USER_ID_LENGTH)
    )

    return f"{USER_ID_PREFIX}{value};"


def generate_team_id():
    length = secrets.randbelow(
        TEAM_ID_MAX_LENGTH - TEAM_ID_MIN_LENGTH + 1
    ) + TEAM_ID_MIN_LENGTH

    characters = [
        secrets.choice(TEAM_ID_ALPHABET)
        for _ in range(length)
    ]

    dot_position = secrets.randbelow(length - 2) + 1
    characters[dot_position] = "."

    characters[0] = secrets.choice(string.digits)
    characters[-1] = secrets.choice(string.digits)

    return "".join(characters)


def validate_user_id(user_id):
    return bool(
        re.fullmatch(
            rf"{re.escape(USER_ID_PREFIX)}[a-z0-9]{{{USER_ID_LENGTH}}};",
            user_id or ""
        )
    )


def validate_team_id(team_id):
    return bool(
        re.fullmatch(
            r"[0-9][A-Za-z0-9]*\.[A-Za-z0-9]*[0-9]",
            team_id or ""
        )
        and TEAM_ID_MIN_LENGTH <= len(team_id) <= TEAM_ID_MAX_LENGTH
    )


def parse_login_identifier(login_identifier):
    if not login_identifier:
        raise ValueError("Login identifier is required.")

    user_end = login_identifier.find(";")

    if user_end == -1:
        raise ValueError("Invalid DarkOps ID format.")

    user_id = login_identifier[:user_end + 1]

    if not validate_user_id(user_id):
        raise ValueError("Invalid DarkOps ID format.")

    remainder = login_identifier[user_end + 1:]

    if not remainder.startswith("++"):
        raise ValueError("Invalid login format.")

    remainder = remainder[2:]

    if "++" not in remainder:
        return {
            "user_id": user_id,
            "password": remainder,
            "team_id": None
        }

    password, team_id = remainder.rsplit("++", 1)

    if not validate_team_id(team_id):
        raise ValueError("Invalid Team ID format.")

    return {
        "user_id": user_id,
        "password": password,
        "team_id": team_id
    }
