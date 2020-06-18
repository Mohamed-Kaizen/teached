"""Collection of services."""
from typing import Any, Dict, Optional

import pendulum

from .models import Student, Teacher, User


async def authenticate(**kwargs: Any) -> Optional[User]:
    """Authenticate function.

    Args:
        kwargs: key word arg.

    Returns:
        user model or None
    """
    password = kwargs.pop("password")
    user = await User.get_or_none(**kwargs)

    if not user:
        return None

    if not user.check_password(plain_password=password):
        return None

    return user


async def update_last_login(*, user: User) -> None:
    """Update user last login.

    Args:
        user: user model
    """
    user.last_login = pendulum.now()
    await user.save()


async def create_user(*, data: Dict) -> None:
    """Create new user.

    Args:
        data: Dict of new user info.
    """
    become = data.pop("become")

    password = data.pop("password")

    user = User(**data)

    user.set_password(plain_password=password)

    await user.save()

    if become.value == "Teacher":
        await Teacher.create(user=user)

    if become.value == "Student":
        await Student.create(user=user)
