import hashlib
import mimetypes
import os
from pathlib import Path

from flask import current_app

from api.integrations import storage_provider


class StorageServiceError(Exception):
    pass


PLAN_STORAGE_CONFIG = {
    "darkops glacier": "DARKOPS_GLACIER_STORAGE_BYTES",
    "darkops nightwatch": "DARKOPS_NIGHTWATCH_STORAGE_BYTES",
    "darkops core": "DARKOPS_CORE_STORAGE_BYTES",
}

SUPPORT_ATTACHMENT_MAX_BYTES = int(
    os.getenv(
        "DARKOPS_SUPPORT_ATTACHMENT_MAX_BYTES",
        10 * 1024 * 1024,
    )
)

MAX_UPLOAD_BYTES = int(
    os.getenv(
        "DARKOPS_MAX_UPLOAD_BYTES",
        100 * 1024 * 1024,
    )
)

ALLOWED_ASSET_TYPES = {
    "security_document",
    "api_specification",
    "security_log",
    "incident_report",
    "architecture_document",
    "dependency_report",
    "configuration_document",
    "security_evidence",
}

ALLOWED_ATTACHMENT_MIME_PREFIXES = (
    "image/",
    "video/",
    "audio/",
)

ALLOWED_DOCUMENT_MIME_TYPES = {
    "application/pdf",
    "application/json",
    "application/xml",
    "text/plain",
    "text/csv",
    "text/xml",
    "application/zip",
    "application/gzip",
}


def _plan_key(plan_name):
    if not plan_name or not isinstance(plan_name, str):
        raise StorageServiceError("A subscription plan is required.")

    key = plan_name.strip().lower()

    if key not in PLAN_STORAGE_CONFIG:
        raise StorageServiceError(
            f"Unsupported DarkOps storage plan: {plan_name}"
        )

    return key


def get_plan_storage_limit(plan_name):
    config_key = PLAN_STORAGE_CONFIG[_plan_key(plan_name)]
    value = current_app.config.get(config_key)

    if value is None:
        value = os.getenv(config_key)

    if value is None:
        raise StorageServiceError(
            f"Storage capacity for {plan_name} has not been configured."
        )

    try:
        value = int(value)
    except (TypeError, ValueError):
        raise StorageServiceError(
            f"Invalid storage capacity configured for {plan_name}."
        )

    if value < 0:
        raise StorageServiceError(
            f"Storage capacity for {plan_name} cannot be negative."
        )

    return value


def validate_size(size_bytes, maximum_bytes=None):
    if size_bytes is None:
        raise StorageServiceError("File size could not be determined.")

    if size_bytes < 0:
        raise StorageServiceError("File size cannot be negative.")

    maximum_bytes = (
        maximum_bytes
        if maximum_bytes is not None
        else MAX_UPLOAD_BYTES
    )

    if size_bytes > maximum_bytes:
        raise StorageServiceError(
            f"File exceeds the maximum allowed size of {maximum_bytes} bytes."
        )

    return True


def validate_attachment_type(filename, mime_type=None):
    mime_type = (
        mime_type
        or mimetypes.guess_type(filename or "")[0]
        or "application/octet-stream"
    ).lower()

    if (
        mime_type not in ALLOWED_DOCUMENT_MIME_TYPES
        and not mime_type.startswith(ALLOWED_ATTACHMENT_MIME_PREFIXES)
    ):
        raise StorageServiceError(
            f"Unsupported attachment type: {mime_type}"
        )

    return mime_type


def validate_asset_type(asset_type):
    if asset_type not in ALLOWED_ASSET_TYPES:
        raise StorageServiceError(
            f"Unsupported security asset type: {asset_type}"
        )

    return True


def calculate_checksum(file):
    try:
        current_position = file.tell()
    except (AttributeError, OSError):
        current_position = 0

    try:
        file.seek(0)
        digest = hashlib.sha256()

        while True:
            chunk = file.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

        return digest.hexdigest()

    except (AttributeError, OSError) as error:
        raise StorageServiceError(
            "Unable to calculate file checksum."
        ) from error

    finally:
        try:
            file.seek(current_position)
        except (AttributeError, OSError):
            pass


def get_file_size(file):
    try:
        current_position = file.tell()
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(current_position)
        return size
    except (AttributeError, OSError) as error:
        raise StorageServiceError(
            "Unable to determine file size."
        ) from error


def validate_storage_quota(
    current_usage_bytes,
    incoming_size_bytes,
    plan_name,
):
    limit = get_plan_storage_limit(plan_name)

    current_usage_bytes = max(0, int(current_usage_bytes))
    incoming_size_bytes = max(0, int(incoming_size_bytes))

    if current_usage_bytes + incoming_size_bytes > limit:
        raise StorageServiceError(
            f"Storage quota exceeded for {plan_name}."
        )

    return {
        "limit_bytes": limit,
        "current_usage_bytes": current_usage_bytes,
        "incoming_size_bytes": incoming_size_bytes,
        "remaining_bytes": (
            limit
            - current_usage_bytes
            - incoming_size_bytes
        ),
    }


def _folder(owner_key, category):
    safe_owner = str(owner_key).replace("/", "_")
    safe_category = str(category).replace("/", "_")

    return f"darkops/{safe_category}/{safe_owner}"


def upload(
    file,
    owner_key,
    plan_name,
    category,
    current_usage_bytes=0,
    filename=None,
    mime_type=None,
    public_id=None,
    support=False,
):
    if not file:
        raise StorageServiceError("A file is required.")

    filename = filename or getattr(file, "filename", None)

    if not filename:
        raise StorageServiceError("A filename is required.")

    size_bytes = get_file_size(file)

    maximum = (
        SUPPORT_ATTACHMENT_MAX_BYTES
        if support
        else MAX_UPLOAD_BYTES
    )

    validate_size(
        size_bytes,
        maximum_bytes=maximum,
    )

    resolved_mime = validate_attachment_type(
        filename,
        mime_type,
    )

    quota = None

    if not support:
        quota = validate_storage_quota(
            current_usage_bytes,
            size_bytes,
            plan_name,
        )

    checksum = calculate_checksum(file)

    result = storage_provider.upload(
        file=file,
        folder=_folder(
            owner_key,
            category,
        ),
        public_id=public_id,
        resource_type="auto",
        delivery_type="authenticated",
    )

    return {
        "storage": result,
        "filename": filename,
        "mime_type": resolved_mime,
        "size_bytes": size_bytes,
        "checksum_sha256": checksum,
        "category": category,
        "quota": quota,
    }


def upload_large(
    file,
    owner_key,
    plan_name,
    category,
    current_usage_bytes=0,
    filename=None,
    mime_type=None,
    public_id=None,
    support=False,
):
    if not file:
        raise StorageServiceError("A file is required.")

    filename = filename or getattr(file, "filename", None)

    if not filename:
        raise StorageServiceError("A filename is required.")

    size_bytes = get_file_size(file)

    maximum = (
        SUPPORT_ATTACHMENT_MAX_BYTES
        if support
        else MAX_UPLOAD_BYTES
    )

    validate_size(
        size_bytes,
        maximum_bytes=maximum,
    )

    resolved_mime = validate_attachment_type(
        filename,
        mime_type,
    )

    quota = None

    if not support:
        quota = validate_storage_quota(
            current_usage_bytes,
            size_bytes,
            plan_name,
        )

    checksum = calculate_checksum(file)

    result = storage_provider.upload_large(
        file=file,
        folder=_folder(
            owner_key,
            category,
        ),
        public_id=public_id,
        resource_type="auto",
        delivery_type="authenticated",
    )

    return {
        "storage": result,
        "filename": filename,
        "mime_type": resolved_mime,
        "size_bytes": size_bytes,
        "checksum_sha256": checksum,
        "category": category,
        "quota": quota,
    }


def delete(public_id, resource_type="image"):
    if not public_id:
        raise StorageServiceError("A storage identifier is required.")

    return storage_provider.delete(
        public_id=public_id,
        resource_type=resource_type,
        delivery_type="authenticated",
    )


def get_url(public_id, resource_type="image"):
    if not public_id:
        raise StorageServiceError("A storage identifier is required.")

    return storage_provider.get_url(
        public_id=public_id,
        resource_type=resource_type,
        delivery_type="authenticated",
    )
