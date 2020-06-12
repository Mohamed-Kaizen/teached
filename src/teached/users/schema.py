"""Collection of pydantic schema."""
from uuid import UUID

from pydantic import BaseModel


class TokenData(BaseModel):
    """Schema for token data."""

    id: UUID
    username: str
    exp: int
