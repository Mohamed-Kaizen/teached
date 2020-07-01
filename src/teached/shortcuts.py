"""Shortcuts functions for Teached project."""
import importlib
from typing import Any

from .settings import settings


def get_user_model() -> Any:
    """Getting User Model."""
    module_name, class_name = settings.User_MODEL.rsplit(".", 1)

    return getattr(importlib.import_module(module_name), class_name)


def get_model(*, path: str) -> Any:
    """Getting any model."""

    module_name, class_name = path.rsplit(".", 1)

    return getattr(importlib.import_module(module_name), class_name)


def upload_to_dropbox(
    *, oauth2_token: str, file: bytes, filename: str, file_path: str
) -> None:
    """Helper function that upload files to dropbox.

    Args:
        oauth2_token: DropBox token.
        file: The file in bytes.
        filename: The file name.
        file_path: A file path to store in dropbox.
    """
    import dropbox

    dbx = dropbox.Dropbox(oauth2_token)
    dbx.users_get_current_account()
    dbx.files_upload(file, f"{file_path}/{filename}")
