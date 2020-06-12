"""Models for users app."""
from .base import AbstractUser


class User(AbstractUser):
    """The User model."""

    class Meta:
        """Meta data."""

        table = "user"
