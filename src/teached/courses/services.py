"""Collection of services."""
from typing import Dict

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
