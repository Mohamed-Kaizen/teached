"""Collection of utils."""
from typing import Optional

import jwt
import pendulum
from jwt import PyJWTError

from teached.settings import PASSWORD_CONTEXT, logger, settings

from .schema import TokenData  # noqa: I202


def make_password_hash(*, password: str) -> str:
    """Turn a plain-text password into a hash for database storage.

    Args:
        password: plain text

    Example:
        >>> from teached.users import utils
        >>> hashed_password = utils.make_password_hash(password="raw password")
        >>> len(hashed_password) > 0
        True
        >>> type(hashed_password) == str
        True

    Returns:
        Hash string
    """
    return PASSWORD_CONTEXT.hash(password)


def verify_password(*, plain_password: str, hashed_password: str) -> bool:
    """Verify plain-text password.

    Args:
        plain_password: plain text
        hashed_password: hashed string

    Example:
        >>> from teached.users import utils
        >>> hashed_password = utils.make_password_hash(password="raw password")
        >>> utils.verify_password(plain_password="raw password", hashed_password=hashed_password) # noqa: B950
        True

    Returns:
        bool
    """
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def create_access_token(*, data: dict, expires_in_minutes: int) -> bytes:
    """Create access token.

    Args:
        data: Dict to pass to the token.
        expires_in_minutes: For how many minutes will the token will be valid.

    Example:
        >>> from teached.users import utils
        >>> data = {"username": "A"}
        >>> token = utils.create_access_token(data=data, expires_in_minutes=5)
        >>> len(token) > 0
        True
        >>> type(token) == bytes
        True

    Returns:
        access token
    """
    expire = pendulum.now().add(minutes=expires_in_minutes)

    data.update({"exp": expire})

    return jwt.encode(
        payload=data, key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def verified_token(*, token: bytes) -> Optional[TokenData]:
    """Verfiy token.

    Args:
        token: jwt.

    Example:
        >>> from teached.users import utils
        >>> data = {"sub": "A", "exp": 1565, "id": "6f07387f-a42a-4d61-9e72-d76009cb6f68"}  # noqa: B950
        >>> token = utils.create_access_token(data=data, expires_in_minutes=5)
        >>> utils.verified_token(token=token) is not None
        True
        >>> utils.verified_token(token=b"sds") is None
        True

    Returns:
        TokenData pydantic model or None
    """
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=settings.JWT_ALGORITHM,
            verify=True,
        )

        token_data = TokenData(
            username=payload.get("sub"), exp=payload.get("exp"), id=payload.get("id"),
        )

    except PyJWTError as error:
        logger.error(error)
        return None

    return token_data
