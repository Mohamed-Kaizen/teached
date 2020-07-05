"""Collection of depends functions."""
from typing import Tuple

from fastapi import Depends, HTTPException, Request, status

from teached.users.depends import is_teacher
from teached.users.models import Teacher

from .models import Course  # noqa: I202


async def is_owner(
    request: Request, current_user: Teacher = Depends(is_teacher)
) -> Tuple[Teacher, Course]:
    """Check if the user is owner of the course.

    Args:
        request: Request object.
        current_user: depends function.

    Returns:
        teacher and course model

    Raises:
        HTTPException: If user is not teacher return 400 status.
    """
    course = await Course.get(
        is_drift=True, is_active=True, slug=request.path_params.get("slug")
    )

    if await course.teacher != current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission to access.",
        )
    return current_user, course
