"""Collection of depends functions."""
from fastapi import Depends, HTTPException, Request, status

from teached.settings import OAUTH2_SCHEME

from .models import User  # noqa: I202


async def login_required(request: Request, token: str = Depends(OAUTH2_SCHEME)) -> User:
    """Check if the user is authenticated.

    Args:
        request: request object.
        token: in come token.

    Returns:
        user model
    """
    return request.state.user


async def is_superuser(current_user: User = Depends(login_required)) -> User:
    """Check if the user is superuser.

    Args:
        current_user: depends function.

    Returns:
        user model

    Raises:
        HTTPException: If user is not superuser return 404 status.
    """
    if current_user.is_superuser:
        return current_user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not Found")


async def is_active_user(current_user: User = Depends(login_required)) -> User:
    """Check if the user is active.

    Args:
        current_user: depends function.

    Returns:
        user model

    Raises:
        HTTPException: If user is not superuser return 400 status.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
