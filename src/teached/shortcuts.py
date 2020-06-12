"""Shortcuts functions for Teached project."""
import importlib
from typing import Any

from .settings import settings


def get_user_model() -> Any:
    """Getting User Model."""
    module_name, class_name = settings.User_MODEL.rsplit(".", 1)

    return getattr(importlib.import_module(module_name), class_name)
