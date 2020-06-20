"""Collection of pydantic schema."""
import re
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator

from teached.settings import settings

from . import pwned, validators  # noqa: I202


class UserType(str, Enum):
    """Enum class to determine type of user."""

    teacher = "Teacher"

    student = "Student"


class TokenData(BaseModel):
    """Schema for token data."""

    id: UUID
    username: str
    exp: int


class User(BaseModel):
    """Schema for user sign up data."""

    username: str = Field(..., min_length=1, max_length=256)

    password: str = Field(
        ...,
        min_length=settings.MINIMUM_PASSWORD_LENGTH,
        max_length=settings.MAXIMUM_PASSWORD_LENGTH,
    )
    email: EmailStr

    full_name: str = Field("", max_length=100)

    phone_number: str = Field("", min_length=9, max_length=15)

    become: UserType

    @validator("username")
    def extra_validation_on_username(cls: "User", value: str) -> str:  # noqa DAR101
        """Extra Validation for the username.

        Args:
            cls: It the same as self
            value: The username value from an input.

        Returns:
            The username if it is valid.
        """
        validators.validate_reserved_name(value=value, exception_class=ValueError)

        validators.validate_confusables(value=value, exception_class=ValueError)

        return value

    @validator("password")
    def extra_validation_on_password(cls: "User", value: str) -> str:  # noqa DAR101
        """Extra Validation for the password.

        Args:
            cls: It the same as self
            value: The password value from an input.

        Returns:
            The password if it is valid.

        Raises:
            ValueError: If password is pwned or connection error it return 422 status.
        """
        result = pwned.pwned_password(password=value)

        if result is None:
            raise ValueError("Connection error, try again")

        if result > 0:
            raise ValueError(
                f"Oh no — pwned! This password has been seen {result} times before"
            )

        else:
            return value

    @validator("email")
    def extra_validation_on_email(cls: "User", value: str) -> str:  # noqa DAR101
        """Extra Validation for the email.

        Args:
            cls: It the same as self
            value: The email value from an input.

        Returns:
            The email if it is valid.
        """
        local_part, domain = value.split("@")

        validators.validate_reserved_name(value=local_part, exception_class=ValueError)

        validators.validate_confusables_email(
            domain=domain, local_part=local_part, exception_class=ValueError
        )

        return value

    @validator("phone_number")
    def extra_validation_on_phone_number(cls: "User", value: str) -> str:  # noqa DAR101
        """Extra Validation for the phone_number.

        Args:
            cls: It the same as self
            value: The phone_number value from an input.

        Returns:
            The phone_number if it is valid.

        Raises:
            ValueError: If phone number is invalid return 422 status.
        """
        result = re.match(r"^\+?1?\d{9,15}$", value)
        if not result:
            raise ValueError(
                "Phone number must be entered in the format: '+251999999999."
                " Up to 15 digits allowed."
            )
        return value


class UsernameAndEmail(BaseModel):
    """Schema for username and email data."""

    username: str = Field("", min_length=1, max_length=256)

    email: EmailStr = ""

    @validator("username")
    def extra_validation_on_username(
        cls: "UsernameAndEmail", value: str  # noqa DAR101
    ) -> str:  # noqa DAR101
        """Extra Validation for the username.

        Args:
            cls: It the same as self
            value: The username value from an input.

        Returns:
            The username if it is valid.
        """
        validators.validate_reserved_name(value=value, exception_class=ValueError)

        validators.validate_confusables(value=value, exception_class=ValueError)

        return value

    @validator("email")
    def extra_validation_on_email(
        cls: "UsernameAndEmail", value: str  # noqa DAR101
    ) -> str:  # noqa DAR101
        """Extra Validation for the email.

        Args:
            cls: It the same as self
            value: The email value from an input.

        Returns:
            The email if it is valid.
        """
        local_part, domain = value.split("@")

        validators.validate_reserved_name(value=local_part, exception_class=ValueError)

        validators.validate_confusables_email(
            domain=domain, local_part=local_part, exception_class=ValueError
        )

        return value


class Password(BaseModel):
    """Schema for password data."""

    old_password: str = Field(
        ...,
        min_length=settings.MINIMUM_PASSWORD_LENGTH,
        max_length=settings.MAXIMUM_PASSWORD_LENGTH,
    )

    new_password: str = Field(
        ...,
        min_length=settings.MINIMUM_PASSWORD_LENGTH,
        max_length=settings.MAXIMUM_PASSWORD_LENGTH,
    )

    @validator("new_password")
    def extra_validation_on_new_password(
        cls: "Password", value: str  # noqa DAR101
    ) -> str:
        """Extra Validation for the new_password.

        Args:
            cls: It the same as self
            value: The new password value from an input.

        Returns:
            The new password if it is valid.

        Raises:
            ValueError: If new password is pwned or connection error.
        """
        result = pwned.pwned_password(password=value)

        if result is None:
            raise ValueError("Connection error, try again")

        if result > 0:
            raise ValueError(
                f"Oh no — pwned! This password has been seen {result} times before"
            )

        else:
            return value
