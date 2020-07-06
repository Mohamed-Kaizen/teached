"""Collection of services."""
from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
from tortoise import QuerySet

from teached.users.models import Teacher

from .models import (  # noqa I202
    Assignment,
    BookMark,
    Category,
    Course,
    CourseDetailPydantic,
    Enrollment,
    Language,
    Lecture,
    Requirement,
    Review,
    Section,
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


async def create_review_for_published_course(
    *, slug: str, data: Dict, student: Any
) -> Dict[str, str]:
    """Create review for a published course.

    Args:
        slug: The slug of course.
        data: Dict of data for review creation.
        student: Student instances.

    Returns:
        Dict.

    Raises:
        HTTPException: If use has has not enroll for the course or
                       student review the course already.
    """
    course = await Course.get(is_drift=True, is_active=True, slug=slug)

    if not await course.enrollments.filter(student=student):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You need to enroll to the course first",
        )

    if await course.reviews.filter(student=student):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already review this course",
        )
    await Review.create(**data, course=course, student=student)

    return {"detail": "review has been created."}


async def reviews_course_list(*, slug: str) -> List[Dict]:
    """Get all  reviews.

    Args:
        slug: The slug of course.

    Returns:
        List of reviews.
    """
    course = await Course.get(is_drift=True, is_active=True, slug=slug)
    review_list = []

    for review in await course.reviews.all():
        student = await review.student
        user = await student.user
        review_list.append(
            {
                "review": f"{review.review}",
                "rate": {review.rate},
                "user": {"username": user.username},
            }
        )

    return review_list


async def create_course_section(*, data: Dict, course: Course,) -> Dict:
    """Create course section.

    Args:
        data: Dict of data for section creation.
        course: Course instance.

    Returns:
        The create section info.

    Raises:
        HTTPException: if the same section was created before.
    """
    section, created = await Section.get_or_create(**data, course=course)

    if not created:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This section was been created before",
        )

    section.slug = unique_slug(title=section.title)
    await section.save()

    return {
        "title": section.title,
        "objective": section.objective,
        "order": section.order,
        "slug": section.slug,
    }


async def create_section_lecture(*, data: Dict, section_slug: str) -> Dict:
    """Create section lecture.

    Args:
        data: Dict of data for section creation.
        section_slug: The slug of the section.

    Returns:
        The created lecture info.

    Raises:
        HTTPException: if the same lecture was created before.
    """
    section = await Section.get(slug=section_slug)

    lecture, created = await Lecture.get_or_create(**data, section=section)

    if not created:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This lecture was been created before",
        )

    lecture.slug = unique_slug(title=lecture.title)
    await lecture.save()

    return {
        "title": lecture.title,
        "text": lecture.text,
        "video": lecture.video,
        "order": section.order,
        "slug": section.slug,
    }


async def create_section_assignment(*, data: Dict, section_slug: str) -> Dict:
    """Create section assignment.

    Args:
        data: Dict of data for section creation.
        section_slug: The slug of the section.

    Returns:
        The created assignment info.

    Raises:
        HTTPException: if the same assignment was created before.
    """
    section = await Section.get(slug=section_slug)

    assignment, created = await Assignment.get_or_create(**data, section=section)

    if not created:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This assignment was been created before",
        )

    assignment.slug = unique_slug(title=assignment.title)
    await assignment.save()

    return {
        "title": assignment.title,
        "text": assignment.description,
        "file": assignment.file,
        "slug": section.slug,
    }
