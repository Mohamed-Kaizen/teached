"""Views for courses app."""
from typing import Dict, List

from fastapi import APIRouter, Depends, status

from teached.users import depends, models

from . import schema  # noqa I202
from .models import CourseListPydantic
from .services import create_course, get_published_courses

router = APIRouter()


@router.get("/")
async def course_list(
    search: str = None,
    category: str = None,
    language: str = None,
    level: str = None,
    price: str = None,
    discount: str = None,
) -> List[CourseListPydantic]:
    """Courses list."""
    return await CourseListPydantic.from_queryset(
        await get_published_courses(
            search=search,
            category=category,
            language=language,
            level=level,
            price=price,
            discount=discount,
        )
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


#
# @router.get("/{slug}/")
# async def course_detail(slug: str) -> Dict[str, str]:
#     """Course detail."""
#
#     slug = await create_course(
#         data=user_input.dict(exclude_unset=True), teacher=auth_user
#     )
#
#     return {"slug": slug}
