"""Collection of services."""
from typing import Any, Optional

import pendulum

from .models import User


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
