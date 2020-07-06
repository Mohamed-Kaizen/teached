"""Views for courses app."""
from typing import Dict, List, Tuple

from fastapi import APIRouter, Depends, Request, status

from teached.users import depends, models

from . import schema  # noqa I202
from .depends import Course, Teacher, is_owner
from .models import CourseListPydantic
from .services import (
    bookmark_a_published_course,
    create_course,
    create_course_announcement,
    create_course_section,
    create_review_for_published_course,
    create_section_assignment,
    create_section_lecture,
    enroll_to_published_course,
    get_bookmarks,
    get_published_course,
    get_published_courses,
    reviews_course_list,
    update_course_settings,
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


@router.post("/{slug}/review/", status_code=status.HTTP_201_CREATED)
async def course_review(
    user_input: schema.CreateReview,
    slug: str,
    auth_user: models.Student = Depends(depends.is_student),
) -> Dict[str, str]:
    """Create review for a course."""
    return await create_review_for_published_course(
        slug=slug, student=auth_user, data=user_input.dict()
    )


@router.get("/{slug}/review/")
async def get_course_reviews(slug: str) -> List[Dict]:
    """Get all course reviews."""
    return await reviews_course_list(slug=slug)


@router.patch("/{slug}/manage/settings/")
async def course_settings(
    slug: str,
    user_input: schema.CourseSettings,
    auth_user: Teacher = Depends(depends.is_teacher),
) -> Dict:
    """Course settings."""
    return await update_course_settings(
        teacher=auth_user, data=user_input.dict(exclude_unset=True), slug=slug
    )


@router.post("/{slug}/manage/section/")
async def section_create(
    user_input: schema.CreateSection,
    auth_user: Tuple[Teacher, Course] = Depends(is_owner),
) -> Dict:
    """Create new section for a course."""
    _, course = auth_user
    return await create_course_section(course=course, data=user_input.dict())


@router.post("/{slug}/manage/announcement/")
async def announcement_create(
    user_input: schema.CreateAnnouncement,
    auth_user: Tuple[Teacher, Course] = Depends(is_owner),
) -> Dict:
    """Create new announcement for a course."""
    teacher, course = auth_user
    return await create_course_announcement(
        teacher=teacher, course=course, data=user_input.dict()
    )


@router.post("/{slug}/manage/section/{section_slug}/lecture/")
async def lecture_create(
    section_slug: str,
    user_input: schema.CreateLecture,
    auth_user: Tuple[Teacher, Course] = Depends(is_owner),
) -> Dict:
    """Create new lecture for a section."""
    return await create_section_lecture(
        section_slug=section_slug, data=user_input.dict(exclude_unset=True)
    )


@router.post("/{slug}/manage/section/{section_slug}/assignment/")
async def assignment_create(
    section_slug: str,
    user_input: schema.CreateAssignment,
    auth_user: Tuple[Teacher, Course] = Depends(is_owner),
) -> Dict:
    """Create new assignment for a section."""
    return await create_section_assignment(
        section_slug=section_slug, data=user_input.dict(exclude_unset=True)
    )


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
