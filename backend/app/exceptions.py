"""
Centralized exception handling for the application.
Maps domain exceptions to HTTP responses with proper status codes.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import structlog

logger = structlog.get_logger()


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 500, detail: str | None = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)


class NotFoundException(AppException):
    """Resource not found."""

    def __init__(self, resource: str = "Resource", resource_id: str = ""):
        super().__init__(
            message=f"{resource} not found" + (f": {resource_id}" if resource_id else ""),
            status_code=404,
        )


class UnauthorizedException(AppException):
    """Authentication required."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(message=message, status_code=401)


class ForbiddenException(AppException):
    """Insufficient permissions."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message=message, status_code=403)


class ConflictException(AppException):
    """Resource conflict (e.g. duplicate)."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message=message, status_code=409)


class BadRequestException(AppException):
    """Invalid request."""

    def __init__(self, message: str = "Invalid request"):
        super().__init__(message=message, status_code=400)


class RateLimitException(AppException):
    """Rate limit exceeded."""

    def __init__(self, message: str = "Rate limit exceeded. Please try again later."):
        super().__init__(message=message, status_code=429)


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.warning(
            "app_exception",
            message=exc.message,
            status_code=exc.status_code,
            path=str(request.url),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
        logger.warning("validation_error", errors=exc.errors(), path=str(request.url))
        return JSONResponse(
            status_code=422,
            content={
                "error": True,
                "message": "Validation error",
                "detail": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            "unhandled_exception",
            error=str(exc),
            path=str(request.url),
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "Internal server error",
                "detail": None,
            },
        )
