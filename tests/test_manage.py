"""Test cases for the manage module."""
from typer.testing import CliRunner

from teached.manage import app

runner = CliRunner()


def test_help_succeeds() -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "version" in result.output
    assert "create-superuser" in result.output


def test_version_succeeds() -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Teached" in result.stdout


def test_create_superuser_succeeds() -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(
        app,
        ["create-superuser"],
        input="teached\nteached@example.com\n123456\n123456\ny",
    )
    assert result.exit_code == 0
    assert "teached hes been created" in result.stdout
