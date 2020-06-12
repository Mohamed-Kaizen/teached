"""Settings for Teached Project."""
import pathlib
import sys
from typing import List

from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from passlib.context import CryptContext
from pydantic import BaseSettings

BASE_DIR = pathlib.Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    """Base settings for Teached."""

    PROJECT_NAME: str = "Teached"

    PROJECT_DESCRIPTION: str = "online learning platform"

    DOCS_URL: str = "/docs"

    REDOC_URL: str = "/redoc"

    OPENAPI_URL: str = "/openapi.json"

    ALLOWED_HOSTS: List[str] = ["*"]

    DEBUG: bool

    CORS_ORIGINS: List[str] = ["*"]

    CORS_ALLOW_CREDENTIALS: bool = True

    CORS_ALLOW_METHODS: List[str] = ["*"]

    CORS_ALLOW_HEADERS: List[str] = ["*"]

    DATABASE_URL: str = "sqlite://./db.sqlite3"

    DB_MODELS: List[str] = ["teached.users.models"]

    PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    User_MODEL: str = "teached.users.models.User"

    SECRET_KEY: str

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        """Base Config for Settings."""

        env_file = BASE_DIR.joinpath(".env")


settings = Settings()

logger.add(sys.stderr, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/users/login/")

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
