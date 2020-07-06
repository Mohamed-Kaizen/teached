"""Collection of pydantic schema."""
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from .enum import Level


class Course(BaseModel):
    """Schema for course creation data."""

    title: str = Field(..., min_length=1, max_length=100)

    overview: str

    categories: List[str]

    languages: List[str]

    requirements: List[str]

    level: Level

    price: float

    discount: Optional[float] = None


class CourseDetail(BaseModel):
    """Schema for course detail data."""

    title: str

    overview: str

    level: str

    cover: Optional[str]

    video: Optional[str]

    price: float

    discount: float

    enrollments: int

    reviews: int

    rate: int

    created_at: datetime

    updated_at: datetime

    is_authenticated: bool

    has_enroll: bool

    is_owner: bool

    teacher: Dict

    categories: List[Dict]

    languages: List[Dict]

    requirements: List[Dict]

    sections: List[Dict]


class CreateReview(BaseModel):
    """Schema for review creation data."""

    review: str

    rate: int = Field(..., ge=1, le=5)


class CreateSection(BaseModel):
    """Schema for section creation data."""

    title: str = Field(..., max_length=100, min_length=1)

    objective: str

    order: int


class CreateLecture(BaseModel):
    """Schema for lecture creation data."""

    title: str = Field(..., max_length=100, min_length=1)

    text: Optional[str]

    order: int
