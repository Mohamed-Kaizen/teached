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


async def create_user() -> None:
    """Creating user for test."""
    user = User(username="mohamed", email="q@e.com")
    password = "1234567899mnm"
    user.set_password(plain_password=password)
    await user.save()


def test_login(client: TestClient, event_loop: asyncio.AbstractEventLoop) -> None:
    """It exits with a status code of 200."""
    event_loop.run_until_complete(create_user())
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/users/login/", data="username=mohamed&password=1234567899mnm", headers=headers
    )
    assert response.status_code == 200


def test_login_incorrect_password(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 401."""
    event_loop.run_until_complete(create_user())
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/users/login/", data="username=mohamed&password=1234567899mn", headers=headers
    )
    assert response.status_code == 401


def test_login_incorrect(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 401."""
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/users/login/", data="username=mohamed&password=1234567899mnm", headers=headers
    )
    assert response.status_code == 401
