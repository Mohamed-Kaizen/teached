"""Views for courses app."""
from typing import Dict, List

from fastapi import APIRouter, Depends, status

from teached.users import depends, models

from . import schema  # noqa I202
from .models import Course, CourseListPydantic
from .services import create_course

router = APIRouter()


@router.get("/")
async def course_list() -> List[CourseListPydantic]:
    """Courses list."""
    # TODO: Change is_drift to False
    return await CourseListPydantic.from_queryset(
        Course.filter(is_drift=True, is_active=True)
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def course_create(
    user_input: schema.Course, auth_user: models.Teacher = Depends(depends.is_teacher),
) -> Dict[str, str]:
    """Create new course."""
    slug = await create_course(
        data=user_input.dict(exclude_unset=True), teacher=auth_user
    )

    return {"slug": slug}
