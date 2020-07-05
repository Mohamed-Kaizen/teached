"""Enums for courses app."""
from enum import Enum


class Category(str, Enum):
    """Category enum class."""

    finance_accounting = "Finance & Accounting"

    development = "Development"

    business = "Business"

    it_software = "IT Software"

    office_productivity = "Office Productivity"

    personal_development = "Personal Development"

    design = "Design"

    marketing = "Marketing"

    lifestyle = "Lifestyle"

    photography = "Photography"

    health_fitness = "Health Fitness"

    music = "Music"

    teaching_academics = "Teaching Academics"


class Level(str, Enum):
    """Level enum class."""

    Beginner = "beginner"

    Intermediate = "intermediate"

    Expert = "expert"

    All = "all"
