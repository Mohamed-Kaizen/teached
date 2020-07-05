"""Collection of pydantic schema."""
from typing import List, Optional

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
