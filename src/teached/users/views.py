"""Views for users app."""
from typing import Dict, Union

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from teached.settings import settings

from . import schema, utils  # noqa: I202
from .services import authenticate, create_user, update_last_login

router = APIRouter()


@router.post("/login/")
async def login(
    background_tasks: BackgroundTasks, form_data: OAuth2PasswordRequestForm = Depends(),
) -> Dict[str, Union[bytes, str]]:
    """Login End point."""
    user = await authenticate(username=form_data.username, password=form_data.password)

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

    background_tasks.add_task(update_last_login, user=user)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def sign_up(user_input: schema.User) -> Dict[str, str]:
    """Sign up new users."""
    await create_user(data=user_input.dict())
    return {"detail": "user has been created"}
