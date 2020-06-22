"""Models for users app."""
from tortoise import Tortoise, fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

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

    id = fields.UUIDField(pk=True)

    user = fields.OneToOneField(
        "models.User", related_name="teachers", on_delete=fields.CASCADE
    )

    class Meta:
        """Meta data."""

        table = "teacher"


class Student(models.Model):
    """The student model."""

    id = fields.UUIDField(pk=True)

    user = fields.OneToOneField(
        "models.User", related_name="students", on_delete=fields.CASCADE
    )

    class Meta:
        """Meta data."""

        table = "student"


Tortoise.init_models(["teached.users.models"], "models")
UserPydantic = pydantic_model_creator(
    User, name="User", exclude=("password", "id", "is_superuser")
)
UserPersonalInfoPydantic = pydantic_model_creator(
    User,
    name="UserIn",
    include=("full_name", "phone_number", "bio"),
    exclude_readonly=True,
)
