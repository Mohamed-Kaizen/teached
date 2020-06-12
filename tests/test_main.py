"""Test cases for the main module."""
from fastapi.testclient import TestClient

from teached.main import app

client = TestClient(app)


def test_docs_url() -> None:
    """It exits with a status code of 200."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_url() -> None:
    """It exits with a status code of 200."""
    response = client.get("/redoc")
    assert response.status_code == 200


def test_openapi_url() -> None:
    """It exits with a status code of 200."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
