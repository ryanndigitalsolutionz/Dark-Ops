import os

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()


class StorageProviderError(Exception):
    pass


def _configure():
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")

    if not all([cloud_name, api_key, api_secret]):
        raise StorageProviderError(
            "Cloudinary credentials are not configured."
        )

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )


def upload(
    file,
    folder,
    public_id=None,
    resource_type="auto",
    delivery_type="authenticated",
):
    _configure()

    options = {
        "folder": folder,
        "resource_type": resource_type,
        "type": delivery_type,
        "secure": True,
    }

    if public_id:
        options["public_id"] = public_id

    try:
        return cloudinary.uploader.upload(
            file,
            **options,
        )
    except Exception as error:
        raise StorageProviderError(
            f"Cloudinary upload failed: {error}"
        ) from error


def upload_large(
    file,
    folder,
    public_id=None,
    resource_type="auto",
    delivery_type="authenticated",
    chunk_size=20_000_000,
):
    _configure()

    options = {
        "folder": folder,
        "resource_type": resource_type,
        "type": delivery_type,
        "secure": True,
        "chunk_size": chunk_size,
    }

    if public_id:
        options["public_id"] = public_id

    try:
        return cloudinary.uploader.upload_large(
            file,
            **options,
        )
    except Exception as error:
        raise StorageProviderError(
            f"Cloudinary large-file upload failed: {error}"
        ) from error


def delete(
    public_id,
    resource_type="image",
    delivery_type="authenticated",
):
    _configure()

    try:
        return cloudinary.uploader.destroy(
            public_id,
            resource_type=resource_type,
            type=delivery_type,
        )
    except Exception as error:
        raise StorageProviderError(
            f"Cloudinary deletion failed: {error}"
        ) from error


def get_url(
    public_id,
    resource_type="image",
    delivery_type="authenticated",
):
    _configure()

    try:
        result = cloudinary.CloudinaryResource(
            public_id,
            resource_type=resource_type,
            type=delivery_type,
        )

        return result.build_url(
            secure=True,
        )
    except Exception as error:
        raise StorageProviderError(
            f"Cloudinary URL generation failed: {error}"
        ) from error
