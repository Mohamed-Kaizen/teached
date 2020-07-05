"""Collection of services."""
from typing import Dict, Optional

from tortoise import QuerySet

from teached.users.models import Teacher

from .models import Category, Course, Language, Requirement  # noqa I202
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
