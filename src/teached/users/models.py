"""Models for users app."""
from tortoise import fields, models

from .base import AbstractUser


class User(AbstractUser):
    """The User model."""

    full_name = fields.CharField(max_length=100, null=True)

    phone_number = fields.CharField(max_length=15, null=True)

    bio = fields.TextField(null=True)

    class Meta:
        """Meta data."""

        table = "user"


class Teacher(models.Model):
    """The teacher model."""

    user = models.OneToOneFieldInstance(
        "models.User", related_name="teachers", on_delete=fields.CASCADE
    )

    class Meta:
        """Meta data."""

        table = "teacher"


class Student(models.Model):
    """The student model."""

    user = models.OneToOneFieldInstance(
        "models.User", related_name="students", on_delete=fields.CASCADE
    )

    class Meta:
        """Meta data."""

        table = "student"
