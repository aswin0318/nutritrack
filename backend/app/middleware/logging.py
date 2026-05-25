"""Structured logging middleware."""

import time
import uuid

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs all incoming requests and outgoing responses."""

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        # Bind request context
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=str(request.url.path),
            client_ip=request.client.host if request.client else "unknown",
        )

        logger.info("request_started")

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            logger.info(
                "request_completed",
                status_code=response.status_code,
                duration_ms=round(process_time * 1000, 2),
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
            return response

        except Exception as exc:
            process_time = time.time() - start_time
            logger.error(
                "request_failed",
                error=str(exc),
                duration_ms=round(process_time * 1000, 2),
            )
            raise


def setup_logging(app: FastAPI) -> None:
    """Configure structured logging."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if not get_settings_safe() else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(20),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_settings_safe():
    """Safely check if production."""
    try:
        from app.config import get_settings
        return get_settings().is_production
    except Exception:
        return False
