"""Views for users app."""
from typing import Dict, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from teached.settings import settings

from . import services, utils  # noqa: I202

router = APIRouter()


@router.post("/login/")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Dict[str, Union[bytes, str]]:
    """Login End point."""
    user = await services.authenticate(
        username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = utils.create_access_token(
        data={"sub": user.username, "id": f"{user.id}"},
        expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    await services.update_last_login(user=user)

    return {"access_token": access_token, "token_type": "bearer"}
