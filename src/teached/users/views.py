"""Views for users app."""
from typing import Dict, Optional, Union

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from tortoise.contrib.fastapi import HTTPNotFoundError

from teached.settings import settings

from . import depends, schema, utils  # noqa: I202
from .models import User, UserPersonalInfoPydantic, UserPydantic
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


@router.get(
    "/{username}/",
    response_model=UserPydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_user(username: str) -> UserPydantic:
    """Get user info."""
    return await UserPydantic.from_queryset_single(User.get(username=username))


@router.patch(
    "/{username}/personal/",
    response_model=UserPydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_personal_info(
    username: str,
    user: UserPersonalInfoPydantic,
    auth_user: depends.is_active_user = Depends(),
) -> Optional[Response]:
    """Update user personal info."""
    if auth_user.username == username:
        await UserPydantic.from_queryset_single(User.get(username=username))
        await User.filter(username=username).update(**user.dict(exclude_unset=True))
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.patch(
    "/{username}/general/", responses={404: {"model": HTTPNotFoundError}},
)
async def update_general_info(
    username: str,
    user: schema.UsernameAndEmail,
    auth_user: depends.is_active_user = Depends(),
) -> Optional[Response]:
    """Update user general info."""
    if auth_user.username == username:

        await UserPydantic.from_queryset_single(User.get(username=username))
        await User.filter(username=username).update(**user.dict(exclude_unset=True))
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.put(
    "/{username}/password/", responses={404: {"model": HTTPNotFoundError}},
)
async def update_password(
    username: str,
    passwords: schema.Password,
    auth_user: depends.is_active_user = Depends(),
) -> Union[Dict[str, str], Optional[Response]]:
    """Update user password."""
    user = await User.get_or_none(username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if auth_user.username == username:

        if user.check_password(plain_password=passwords.old_password):
            user.set_password(plain_password=passwords.new_password)
            await user.save()
            return {"detail": "password has been changed"}

        return Response("incorrect password", status_code=status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_404_NOT_FOUND)
