"""Collection of utils functions."""
import secrets
import string

from teached.settings import settings

chars_string = string.ascii_lowercase + string.digits + string.ascii_uppercase


def slugify(*, value: str) -> str:
    r"""Slugify function.

    Args:
        value: string to slugify.

    Examples:
        >>> from teached.courses.utils import slugify
        >>> title = "super long_title/to\\slugify@it"
        >>> slugify(value=title)
        super-long-title-to-slugify-it

    Returns:
        The slugify text.
    """
    return (
        value.replace(" ", "-")
        .replace("_", "-")
        .replace("/", "-")
        .replace("\\", "-")
        .replace("@", "-")
    )


def random_string(
    *,
    size: int = getattr(settings, "SLUG_ADDITIONAL_SIZE", 6),
    chars: str = getattr(settings, "SLUG_RANDOM_CHARS", chars_string),
) -> str:
    """Generate random string.

    Args:
        size: Size of the random sting.
        chars: A sting of chars to use.

    Examples:
        >>> from teached.courses.utils import random_string
        >>> len(random_string(size=6)) == 6
        True

    Returns:
        Random string.

    """
    return "".join(secrets.choice(chars) for _ in range(size))


def unique_slug(*, title: str, new_slug: str = None) -> str:
    """Create unique slug.

    Args:
        title: The text where the slug will be generate.
        new_slug: Custom slug to hard code.

    Examples:
        >>> from teached.courses.utils import unique_slug
        >>> len(unique_slug(title="title")) == 12
        True
        >>> unique_slug(title="title", new_slug="default-slug") == "default-slug"
        True


    Returns:
        The created slug or hard code slug
    """
    if new_slug is None:

        slug = slugify(value=title)

        new_slug = f"{slug}-{random_string()}"

    return new_slug
