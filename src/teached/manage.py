"""Command-line interface."""
from typing import Dict

import typer
import uvicorn
from tortoise import Tortoise, run_async

from . import __version__
from .settings import settings
from .shortcuts import get_user_model

app = typer.Typer(help="Teached CLI.")


async def run_tortoise(*, data: Dict, db_url: str = "sqlite://:memory:") -> None:
    """Run tortoise-orm.

    Args:
        data: dict of user input.
        db_url: database URL.
    """
    User = get_user_model()

    await Tortoise.init(db_url=db_url, modules={"models": settings.DB_MODELS})

    await Tortoise.generate_schemas()
    password = data.pop("password")
    user = User(**data)
    user.set_password(plain_password=password)
    await user.save()
    typer.secho(f"{user} hes been created", fg=typer.colors.BRIGHT_GREEN)


@app.command()
def version() -> None:
    """Show project Version."""
    project_name = "Teached"
    typer.secho(f"{project_name} Version: {__version__}", fg=typer.colors.BRIGHT_GREEN)


@app.command()
def serve() -> None:
    """Serve the app."""
    typer.echo("Running the server")

    uvicorn.run(
        "teached.main:app", host="127.0.0.1", port=8000, reload=True, log_level="info",
    )


@app.command("create-superuser")
def create_superuser(
    username: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(
        ..., prompt=True, confirmation_prompt=True, hide_input=True
    ),
    is_test: bool = typer.Option(..., prompt=True),
) -> None:
    """Create super user.

    Args:
        username: prompt user to enter username
        email: prompt user to enter email
        password: prompt user to enter password with confirmation
        is_test: checking if the creation is test env or not
    """
    run_async(
        run_tortoise(
            data={
                "username": username,
                "password": password,
                "email": email,
                "is_superuser": True,
                "is_active": True,
            },
            db_url="sqlite://:memory:" if is_test else settings.DATABASE_URL,
        )
    )


if __name__ == "__main__":
    app()
