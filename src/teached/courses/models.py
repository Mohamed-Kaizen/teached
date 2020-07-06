"""Models for courses app."""
from tortoise import Tortoise, fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from teached.shortcuts import get_model

from .enum import Level  # noqa I202

Teacher = get_model(path="teached.users.models.Teacher")
Student = get_model(path="teached.users.models.Student")


class Language(models.Model):
    """The language model."""

    name = fields.CharField(max_length=200, unique=True)

    class Meta:
        """Meta data."""

        table = "language"

    def __str__(self: "Language") -> str:
        """The string representative for course class."""
        return f"{self.name}"


class Category(models.Model):
    """The category model."""

    name = fields.CharField(max_length=200, unique=True)

    class Meta:
        """Meta data."""

        table = "category"

    def __str__(self: "Category") -> str:
        """The string representative for course class."""
        return f"{self.name}"


class Course(models.Model):
    """The course model."""

    id = fields.UUIDField(pk=True)

    title = fields.CharField(max_length=100)

    overview = fields.TextField()

    cover = fields.CharField(null=True, max_length=500)

    video = fields.CharField(null=True, max_length=500)

    categories = fields.ManyToManyField("models.Category", related_name="courses")

    languages = fields.ManyToManyField("models.Language", related_name="courses")

    level = fields.CharEnumField(enum_type=Level, max_length=100)

    teacher = fields.ForeignKeyField(
        model_name="models.Teacher",
        related_name="courses",
        on_delete=fields.SET_NULL,
        null=True,
    )

    price = fields.FloatField(default=0)

    discount = fields.FloatField(default=0)

    is_drift = fields.BooleanField(default=True)

    is_active = fields.BooleanField(default=True)

    slug = fields.CharField(unique=True, max_length=200)

    created_at = fields.DatetimeField(auto_now_add=True)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta data."""

        table = "course"

    def __str__(self: "Course") -> str:
        """The string representative for course class."""
        return f"{self.title}"


class Requirement(models.Model):
    """The requirement model."""

    id = fields.UUIDField(pk=True)

    name = fields.CharField(max_length=100)

    course = fields.ForeignKeyField(
        model_name="models.Course",
        related_name="requirements",
        on_delete=fields.CASCADE,
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta data."""

        table = "requirement"

    def __str__(self: "Requirement") -> str:
        """The string representative for course class."""
        return f"{self.name} for {self.course}"


class Section(models.Model):
    """The section model."""

    id = fields.UUIDField(pk=True)

    title = fields.CharField(max_length=100)

    objective = fields.TextField()

    course = fields.ForeignKeyField(
        model_name="models.Course", on_delete=fields.CASCADE, related_name="sections",
    )

    order = models.IntField()

    slug = fields.CharField(unique=True, max_length=200, null=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta data."""

        table = "section"

    def __str__(self: "Section") -> str:
        """The string representative for course class."""
        return f"Section {self.order}: {self.title}"


class Lecture(models.Model):
    """The lecture model."""

    id = fields.UUIDField(pk=True)

    title = fields.CharField(max_length=100)

    text = fields.TextField(null=True)

    video = fields.CharField(null=True, max_length=200)

    section = fields.ForeignKeyField(
        model_name="models.Section", on_delete=fields.CASCADE, related_name="lectures",
    )

    order = models.IntField()

    slug = fields.CharField(unique=True, max_length=200, null=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta data."""

        table = "lecture"

    def __str__(self: "Lecture") -> str:
        """The string representative for course class."""
        return f"{self.title}"


class Review(models.Model):
    """The review model."""

    id = fields.UUIDField(pk=True)

    course = fields.ForeignKeyField(
        model_name="models.Course", on_delete=fields.CASCADE, related_name="reviews"
    )

    rate = fields.IntField()

    review = fields.TextField()

    student = fields.ForeignKeyField(
        model_name="models.Student",
        related_name="reviews",
        on_delete=fields.SET_NULL,
        null=True,
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta data."""

        table = "review"

    def __str__(self: "Review") -> str:
        """The string representative for course class."""
        return f"{self.course} by {self.student}"


class BookMark(models.Model):
    """The bookmark model."""

    id = fields.UUIDField(pk=True)

    course = fields.ForeignKeyField(
        model_name="models.Course", related_name="book_marks", on_delete=fields.CASCADE,
    )

    student = fields.ForeignKeyField(
        model_name="models.Student",
        related_name="book_marks",
        on_delete=fields.CASCADE,
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta data."""

        table = "bookmark"

    def __str__(self: "BookMark") -> str:
        """The string representative for course class."""
        return f"book marked {self.course} for {self.student}"


class Enrollment(models.Model):
    """The enrollment model."""

    id = fields.UUIDField(pk=True)

    course = fields.ForeignKeyField(
        model_name="models.Course",
        related_name="enrollments",
        on_delete=fields.CASCADE,
    )

    student = fields.ForeignKeyField(
        model_name="models.Student",
        related_name="enrollments",
        on_delete=fields.CASCADE,
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta data."""

        table = "enrollment"

    def __str__(self: "Enrollment") -> str:
        """The string representative for course class."""
        return f"{self.student} enrollment for {self.course}"


class Certificate(models.Model):
    """The certificate model."""

    id = fields.UUIDField(pk=True)

    name = fields.TextField()

    file = fields.TextField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta data."""

        table = "certificate"

    def __str__(self: "Certificate") -> str:
        """The string representative for course class."""
        return f"{self.name}"


class Announcement(models.Model):
    """The announcement model."""

    id = fields.UUIDField(pk=True)

    title = fields.CharField(max_length=100)

    description = fields.TextField()

    teacher = fields.ForeignKeyField(
        model_name="models.Teacher",
        related_name="announcements",
        on_delete=fields.CASCADE,
        null=False,
    )

    course = fields.ForeignKeyField(
        model_name="models.Course",
        related_name="announcements",
        on_delete=fields.CASCADE,
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta data."""

        table = "announcement"

    def __str__(self: "Announcement") -> str:
        """The string representative for course class."""
        return f"{self.title}"


class Assignment(models.Model):
    """The assignment model."""

    id = fields.UUIDField(pk=True)

    title = fields.CharField(max_length=100)

    description = fields.TextField()

    file = fields.TextField(null=True)

    section = fields.ForeignKeyField(
        model_name="models.Section",
        related_name="assignments",
        on_delete=fields.CASCADE,
    )

    slug = fields.CharField(unique=True, max_length=200, null=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta data."""

        table = "assignment"

    def __str__(self: "Assignment") -> str:
        """The string representative for course class."""
        return f"{self.title}"


Tortoise.init_models(["teached.courses.models"], "models")
CourseListPydantic = pydantic_model_creator(
    Course,
    name="CourseList",
    exclude=(
        "id",
        "overview",
        "video",
        "is_drift",
        "is_active",
        "enrollments",
        "requirements",
        "reviews",
        "is_active",
        "languages.id",
        "requirements.id",
        "categories.id",
        "teacher.id",
        "announcements",
        "sections",
        "book_marks",
        "teacher.announcements",
        "teacher.user.id",
        "teacher.user.password",
        "teacher.user.email",
        "teacher.user.is_superuser",
        "teacher.user.is_active",
        "teacher.user.last_login",
        "teacher.user.joined_at",
        "teacher.user.full_name",
        "teacher.user.phone_number",
        "teacher.user.bio",
        "teacher.user.students",
    ),
)

CourseDetailPydantic = pydantic_model_creator(
    Course,
    name="CourseDetail",
    exclude=(
        "id",
        "slug",
        "is_drift",
        "is_active",
        "announcements",
        "enrollments",
        "reviews",
        "teacher.id",
        "teacher.announcements",
        "teacher.user.id",
        "teacher.user.email",
        "teacher.user.password",
        "teacher.user.is_superuser",
        "teacher.user.is_active",
        "teacher.user.last_login",
        "teacher.user.joined_at",
        "teacher.user.full_name",
        "teacher.user.phone_number",
        "teacher.user.bio",
        "teacher.user.students",
    ),
)
