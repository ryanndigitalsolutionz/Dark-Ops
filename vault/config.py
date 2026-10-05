import os

from dotenv import load_dotenv

load_dotenv()


def env_bool(name, default=False):
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_int(name, default=None):
    value = os.getenv(name)

    if value is None or value.strip() == "":
        return default

    return int(value)


class Config:
    # Flask / database
    SECRET_KEY = os.getenv("DARKOPS_FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DARKOPS_DATABASE_URL",
        "sqlite:///darkops.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Legacy / transitional JWT configuration
    JWT_SECRET_KEY = os.getenv("DARKOPS_JWT_SECRET_KEY")

    # Cloudflare Turnstile
    TURNSTILE_SECRET_KEY = os.getenv("TURNSTILE_SECRET_KEY")
    CLOUDFLARE_ENDPOINT = os.getenv(
        "CLOUDFLARE_ENDPOINT",
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
    )

    # Google authentication
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URL = os.getenv("GOOGLE_REDIRECT_URL")

    # Microsoft authentication
    MICROSOFT_TENANT_ID = os.getenv("MICROSOFT_TENANT_ID")
    MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
    MICROSOFT_CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
    MICROSOFT_REDIRECT_URL = os.getenv("MICROSOFT_REDIRECT_URL")

    # Storage
    DARKOPS_GLACIER_STORAGE_BYTES = env_int(
        "DARKOPS_GLACIER_STORAGE_BYTES",
        0,
    )
    DARKOPS_NIGHTWATCH_STORAGE_BYTES = env_int(
        "DARKOPS_NIGHTWATCH_STORAGE_BYTES",
        0,
    )
    DARKOPS_CORE_STORAGE_BYTES = env_int(
        "DARKOPS_CORE_STORAGE_BYTES",
        0,
    )

    # Cloudinary
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    # Paystack
    PAYSTACK_LIVE_PUBLIC_KEY = os.getenv("PAYSTACK_LIVE_PUBLIC_KEY")
    PAYSTACK_LIVE_SECRET_KEY = os.getenv("PAYSTACK_LIVE_SECRET_KEY")
    PAYSTACK_LIVE_WEBHOOK_URL = os.getenv("PAYSTACK_LIVE_WEBHOOK_URL")

    # Email / SMTP
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = env_int("MAIL_PORT", 587)
    MAIL_USE_TLS = env_bool("MAIL_USE_TLS", True)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_APP_PASSWORD = os.getenv("MAIL_APP_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER",
        MAIL_USERNAME,
    )

    # SMS
    TERMII_API_KEY = os.getenv("TERMII_API_KEY")

    # External intelligence / research
    BRAVE_SEARCH_API = os.getenv("BRAVE_SEARCH_API")
    REST_COUNTRIES_API_KEY = os.getenv("REST_COUNTRIES_API_KEY")
    IPINFO_API_TOKEN = os.getenv("IPINFO_API_TOKEN")

    # General DarkOps storage / uploads
    DARKOPS_MAX_UPLOAD_BYTES = env_int(
        "DARKOPS_MAX_UPLOAD_BYTES",
        100 * 1024 * 1024,
    )
    DARKOPS_SUPPORT_ATTACHMENT_MAX_BYTES = env_int(
        "DARKOPS_SUPPORT_ATTACHMENT_MAX_BYTES",
        10 * 1024 * 1024,
    )

    # Extension
    DARKOPS_EXTENSION_NAME = os.getenv(
        "DARKOPS_EXTENSION_NAME",
        "DarkOps Extension",
    )
    DARKOPS_EXTENSION_VERSION = os.getenv(
        "DARKOPS_EXTENSION_VERSION",
        "1.0.0",
    )
