"""App for Teached Project."""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from . import __version__
from .courses import classroom_views
from .courses import views as courses_views
from .settings import settings
from .users import views as users_views
from .users.middleware import AuthJWTMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=__version__,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)
app.add_middleware(AuthJWTMiddleware)

register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": settings.DB_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(users_views.router, prefix="/users", tags=["users"])
app.include_router(courses_views.router, prefix="/courses", tags=["courses"])
app.include_router(classroom_views.router, prefix="/my-classroom", tags=["classroom"])
