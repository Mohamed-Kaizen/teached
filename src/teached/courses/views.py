"""Views for courses app."""
from typing import Dict, List

from fastapi import APIRouter, Depends, Request, status

from teached.users import depends, models

from . import schema  # noqa I202
from .models import CourseListPydantic
from .services import (
    bookmark_a_published_course,
    create_course,
    enroll_to_published_course,
    get_bookmarks,
    get_published_course,
    get_published_courses,
)

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


@router.get("/bookmarks/")
async def bookmark_list(
    auth_user: models.Student = Depends(depends.is_student),
) -> List[Dict]:
    """List of Bookmark."""
    return await get_bookmarks(student=auth_user)


@router.post("/{slug}/bookmark/", status_code=status.HTTP_201_CREATED)
async def course_bookmark(
    slug: str, auth_user: models.Student = Depends(depends.is_student)
) -> Dict[str, str]:
    """Bookmark a course."""
    return await bookmark_a_published_course(slug=slug, student=auth_user)


@router.get("/{slug}/", response_model=schema.CourseDetail)
async def course_detail(request: Request, slug: str) -> schema.CourseDetail:
    """Course detail."""
    return await get_published_course(slug=slug, user=request.state.user)


@router.post("/{slug}/", status_code=status.HTTP_201_CREATED)
async def course_enroll(
    slug: str, auth_user: models.Student = Depends(depends.is_student)
) -> Dict[str, str]:
    """Course enroll."""
    return await enroll_to_published_course(slug=slug, student=auth_user)
