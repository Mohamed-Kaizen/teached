"""Views for student classroom."""
from fastapi import APIRouter, Depends

from teached.users import depends, models

from .models import StudentCourseListPydantic  # noqa: I202

router = APIRouter()


@router.get("/")
async def my_courses(
    auth_user: models.Student = Depends(depends.is_student),
) -> StudentCourseListPydantic:
    """List of enrolled courses for a student."""
    return await StudentCourseListPydantic.from_queryset(auth_user.enrollments.all())
