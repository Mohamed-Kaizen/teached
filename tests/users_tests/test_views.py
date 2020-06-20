"""Test cases for the view module."""
import asyncio
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from teached.main import app
from teached.settings import settings
from teached.users.models import User


@pytest.fixture()
def client() -> Generator:
    """Tortoise-orm fixture."""
    initializer(modules=settings.DB_MODELS)
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture()
def event_loop(client: TestClient) -> Generator:
    """Event loop."""
    yield client.task.get_loop()


async def create_user(
    username: str = "teached", email: str = "q@e.com", password: str = "2345678teached@"
) -> None:
    """Creating user for test."""
    user = User(username=username, email=email)
    user.set_password(plain_password=password)
    await user.save()


def test_login(client: TestClient, event_loop: asyncio.AbstractEventLoop) -> None:
    """It exits with a status code of 200."""
    event_loop.run_until_complete(create_user())
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/users/login/",
        data="username=teached&password=2345678teached@",
        headers=headers,
    )
    assert response.status_code == 200


def test_login_incorrect_password(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 401."""
    event_loop.run_until_complete(create_user())
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/users/login/",
        data="username=teached&password=2345678teached2@",
        headers=headers,
    )
    assert response.status_code == 401


def test_login_incorrect(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 401."""
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/users/login/",
        data="username=teached&password=2345678teached@",
        headers=headers,
    )
    assert response.status_code == 401


def test_sign_up_as_teacher(client: TestClient) -> None:
    """It exits with a status code of 201."""
    headers = {"Content-type": "application/json"}
    data = {
        "username": "teached",
        "password": "2345678teached@",
        "email": "teached@teached.com",
        "become": "Teacher",
    }
    response = client.post("/users/", json=data, headers=headers)

    assert response.json() == {"detail": "user has been created"}
    assert response.status_code == 201


def test_sign_up_as_student(client: TestClient) -> None:
    """It exits with a status code of 201."""
    data = {
        "username": "teached",
        "password": "2345678teached@",
        "email": "teached@teached.com",
        "become": "Student",
        "full_name": "teached",
        "phone_number": "123456789",
    }
    response = client.post("/users/", json=data)

    assert response.json() == {"detail": "user has been created"}
    assert response.status_code == 201


def test_sign_up_fail(client: TestClient) -> None:
    """It exits with a status code of 422."""
    data = {
        "username": "teached",
        "password": "123456789",
        "email": "teached@teached.com",
        "become": "Student",
        "full_name": "teached",
        "phone_number": "123456789dd",
    }
    response = client.post("/users/", json=data)

    assert response.status_code == 422


def test_user_detail_succeeds(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 200."""
    event_loop.run_until_complete(create_user())

    response = client.get("/users/teached/")
    assert response.status_code == 200


def test_user_detail_fail(client: TestClient) -> None:
    """It exits with a status code of 404."""
    response = client.get("/users/teached/")

    assert response.status_code == 404


def test_user_detail_invalid_token(client: TestClient) -> None:
    """It exits with a status code of 401."""
    response = client.get(
        "/users/teached/", headers={"Authorization": "Bearer wrong token"},
    )
    assert response.status_code == 401


def test_update_user_personal_info_succeeds(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 200."""
    event_loop.run_until_complete(create_user())
    data = {
        "bio": "teached bio",
        "full_name": "teached",
        "phone_number": "123456789",
    }
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    login_response = client.post(
        "/users/login/",
        data="username=teached&password=2345678teached@",
        headers=headers,
    )
    access_token = login_response.json().get("access_token")

    response = client.patch(
        "/users/teached/personal/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200


def test_update_user_personal_info_unauthorized(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 404."""
    event_loop.run_until_complete(create_user())
    event_loop.run_until_complete(
        create_user(  # noqa S106
            username="teached2", email="teached@a.com", password="2345678teached@"
        )
    )
    data = {
        "bio": "teached 2 bio",
    }

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    login_response = client.post(
        "/users/login/",
        data="username=teached2&password=2345678teached@",
        headers=headers,
    )
    access_token = login_response.json().get("access_token")

    response = client.patch(
        "/users/teached/personal/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


def test_update_user_general_info_succeeds(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 200."""
    event_loop.run_until_complete(create_user())
    data = {"email": "teached@teached.io", "username": "TEAch"}

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    login_response = client.post(
        "/users/login/",
        data="username=teached&password=2345678teached@",
        headers=headers,
    )
    access_token = login_response.json().get("access_token")

    response = client.patch(
        "/users/teached/general/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200


def test_update_user_general_info_unauthorized(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 404."""
    event_loop.run_until_complete(create_user())

    event_loop.run_until_complete(
        create_user(  # noqa S106
            username="teached2", email="teached@a.com", password="2345678teached@"
        )
    )

    data = {"email": "teached@teached.io"}

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    login_response = client.post(
        "/users/login/",
        data="username=teached2&password=2345678teached@",
        headers=headers,
    )
    access_token = login_response.json().get("access_token")

    response = client.patch(
        "/users/teached/general/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


def test_update_user_password_succeeds(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 200."""
    event_loop.run_until_complete(create_user())

    data = {
        "old_password": "2345678teached@",
        "new_password": "2345678teached2@",
    }

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    login_response = client.post(
        "/users/login/",
        data="username=teached&password=2345678teached@",
        headers=headers,
    )
    access_token = login_response.json().get("access_token")

    response = client.put(
        "/users/teached/password/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.json() == {"detail": "password has been changed"}


def test_update_user_password_unauthorized(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 404."""
    event_loop.run_until_complete(create_user())

    event_loop.run_until_complete(
        create_user(  # noqa S106
            username="teached2", email="teached@a.com", password="2345678teached@"
        )
    )

    data = {
        "old_password": "2345678teached@",
        "new_password": "2345678teached2@",
    }
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    login_response = client.post(
        "/users/login/",
        data="username=teached2&password=2345678teached@",
        headers=headers,
    )
    access_token = login_response.json().get("access_token")

    response = client.put(
        "/users/teached/password/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


def test_update_user_password_no_user(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 404."""
    event_loop.run_until_complete(create_user())

    data = {
        "old_password": "2345678teached@",
        "new_password": "2345678teached2@",
    }

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    login_response = client.post(
        "/users/login/",
        data="username=teached&password=2345678teached@",
        headers=headers,
    )
    access_token = login_response.json().get("access_token")

    response = client.put(
        "/users/teached2/password/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.json() == {"detail": "Not Found"}


def test_update_user_password_incorrect_password(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 400."""
    event_loop.run_until_complete(create_user())

    data = {
        "old_password": "2345678teached",
        "new_password": "2345678teached@",
    }

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    login_response = client.post(
        "/users/login/",
        data="username=teached&password=2345678teached@",
        headers=headers,
    )
    access_token = login_response.json().get("access_token")

    response = client.put(
        "/users/teached/password/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_update_user_password_pwned(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 422."""
    event_loop.run_until_complete(create_user())

    data = {
        "old_password": "2345678teached@",
        "new_password": "1234567899",
    }

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    login_response = client.post(
        "/users/login/",
        data="username=teached&password=2345678teached@",
        headers=headers,
    )
    access_token = login_response.json().get("access_token")

    response = client.put(
        "/users/teached/password/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 422
