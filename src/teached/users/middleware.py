"""Collection of middleware."""
from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from . import models, utils


class AuthJWTMiddleware(BaseHTTPMiddleware):
    """JWT middleware."""

    async def dispatch(
        self: "BaseHTTPMiddleware", request: Request, call_next: Callable
    ) -> Response:
        """JWT middleware.

        Args:
            request: Request object
            call_next: callable function

        Returns:
            Response object or  JSONResponse if the token is invalid
        """
        authorization = request.headers.get("authorization")

        if authorization and "Bearer" in authorization:
            token_data = utils.verified_token(token=authorization.split(" ")[1])

            if token_data:

                user = await models.User.get_or_none(id=token_data.id)

                request.state.user = user

                response = await call_next(request)

                return response

            else:
                return JSONResponse(
                    content={"detail": "Invalid authentication credentials"},
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    headers={"WWW-Authenticate": "Bearer"},
                )

        request.state.user = None

        response = await call_next(request)

        return response
