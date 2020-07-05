"""Collection of services."""
from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
from tortoise import QuerySet

from teached.users.models import Teacher

from .models import (  # noqa I202
    BookMark,
    Category,
    Course,
    CourseDetailPydantic,
    Enrollment,
    Language,
    Requirement,
)
from .schema import CourseDetail
from .utils import unique_slug


async def create_course(*, data: Dict, teacher: Teacher) -> str:
    """Create new course.

    Args:
        data: Dict of new user info.
        teacher: Teacher model instance.

    Returns:
        Slug of the course
    """
    languages = data.pop("languages")

    categories = data.pop("categories")

    requirements = data.pop("requirements")

    course = Course(**data, teacher=teacher)

    # TODO: change this to signal
    course.slug = unique_slug(title=data.get("title"))

    await course.save()

    for language in languages:
        value, created = await Language.get_or_create(name=language.capitalize())

        await course.languages.add(value)

    for category in categories:
        value, created = await Category.get_or_create(name=category.capitalize())

        await course.categories.add(value)

    for requirement in requirements:
        await Requirement.create(name=requirement.capitalize(), course=course)

    return course.slug


async def get_published_courses(
    *,
    search: Optional[str] = None,
    category: Optional[str] = None,
    language: Optional[str] = None,
    level: Optional[str] = None,
    price: Optional[str] = None,
    discount: Optional[str] = None,
) -> QuerySet[Course]:
    """Return all published courses.

    Args:
        search: Search courses by title.
        category: Filter by category.
        language: Filter by language.
        level: Filter by level.
        price: Filter by price.
        discount: Filter by discount.

    Returns:
        Query set of course.
    """
    # TODO: change is_drift to False.
    courses = Course.filter(is_drift=True, is_active=True)

    if search:
        courses = courses.filter(title=search)

    if category:
        courses = courses.filter(categories__name=category)

    if language:
        courses = courses.filter(languages__name=language)

    if level:
        courses = courses.filter(level=level)

    if price:
        courses = courses.filter(price=price)

    if discount:
        courses = courses.filter(discount=discount)

    return courses


async def get_published_course(*, slug: str, user: Any) -> CourseDetail:
    """Return a published courses.

    Args:
        slug: The slug of course.
        user: Current authenticated user.

    Returns:
        Query set of course.
    """
    # TODO: change is_drift to False.
    course = await Course.get(is_drift=True, is_active=True, slug=slug)
    pydatic_data = await CourseDetailPydantic.from_tortoise_orm(course)
    data = pydatic_data.dict()
    data.update(
        {
            "is_authenticated": user is not None,
            "has_enroll": False,
            "is_owner": False,
            "enrollments": await course.enrollments.all().count(),
            "reviews": await course.reviews.all().count(),
        }
    )

    if user:
        user_student = await user.students.first()
        user_teacher = await user.teachers.first()

        if user_student:
            data.update(
                {
                    "has_enroll": await course.enrollments.filter(
                        student=user_student
                    ).first()
                    is not None
                }
            )

        author = await course.teacher

        if user_teacher == author:
            data.update({"is_owner": True})

    # TODO: change it to computed method.
    reviews = course.reviews.all()
    try:
        rate = sum(review.rate for review in await reviews) / await reviews.count()

    except ZeroDivisionError:
        rate = 0

    data.update({"rate": rate})

    return CourseDetail(**data)


async def enroll_to_published_course(*, slug: str, student: Any) -> Dict[str, str]:
    """Enroll new student to a published course.

    Args:
        slug: The slug of course.
        student: Student instances.

    Returns:
        Dict.

    Raises:
        HTTPException: If use has already enrolled.
    """
    course = await Course.get(is_drift=True, is_active=True, slug=slug)

    if await course.enrollments.filter(student=student):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You already enrolled to {course}",
        )

    if course.price > 0:
        print("Payment")
        # TODO: add the stripe payment
        # stripe()

        # TODO: add payment process to the payment model
        # Payment()

    await Enrollment.create(course=course, student=student)

    return {
        "detail": f"Yea! you have enrolled to {course}, go and enjoy the course now :)"
    }


async def bookmark_a_published_course(*, slug: str, student: Any) -> Dict[str, str]:
    """Bookmark a published course.

    Args:
        slug: The slug of course.
        student: Student instances.

    Returns:
        Dict.

    Raises:
        HTTPException: If use has already bookmarked.
    """
    course = await Course.get(is_drift=True, is_active=True, slug=slug)

    if await course.book_marks.filter(course=course, student=student):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You already bookmark {course}",
        )

    await BookMark.create(course=course, student=student)

    return {"detail": f"{course} has been bookmarked :)"}


async def get_bookmarks(*, student: Any) -> List[Dict]:
    """Get list of bookmark.

    Args:
        student: Student instances.

    Returns:
        List of bookmarked course.
    """
    course_list = []
    for bookmark in await BookMark.filter(student=student):
        course = await bookmark.course
        course_list.append(
            {"title": f"{course.title}", "cover": {course.cover}, "slug": course.slug}
        )
    return course_list
