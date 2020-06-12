"""Collection of Abstraction."""
from tortoise import fields, models

from .utils import make_password_hash, verify_password


class AbstractUser(models.Model):
    """Abstract base user model."""

    id = fields.UUIDField(pk=True)

    username = fields.CharField(max_length=256, unique=True)

    email = fields.CharField(max_length=254, unique=True)

    password = fields.CharField(max_length=128)

    is_superuser = fields.BooleanField(default=False)

    is_active = fields.BooleanField(default=True)

    last_login = fields.DatetimeField(null=True)

    joined_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        """Meta data."""

        abstract = True

    def __str__(self: "AbstractUser") -> str:
        """The string representative."""
        return f"{self.username}"

    def set_password(self: "AbstractUser", *, plain_password: str) -> None:
        """Set password after hashing plain password.

        Args:
            plain_password: plain text.

        Example:
            >>> from teached.users import base
            >>> user = base.AbstractUser()
            >>> user.set_password(plain_password="raw password")
            >>> len(user.password) > 0
            True
            >>> type(user.password) == str
            True
        """
        self.password = make_password_hash(password=plain_password)

    def check_password(self: "AbstractUser", *, plain_password: str) -> bool:
        """Check plain text.

        Return a boolean of whether the plain_password was correct.
        Handles hashing formats behind the scenes.

        Args:
            plain_password: plain text.

        Example:
            >>> from teached.users import base
            >>> user = base.AbstractUser()
            >>> user.set_password(plain_password="raw password")
            >>> user.check_password(plain_password="raw password")
            True

        Returns:
            bool
        """
        return verify_password(
            plain_password=plain_password, hashed_password=self.password
        )
