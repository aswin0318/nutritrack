"""
NutriTrack360 Backend Application Entry Point.
FastAPI application with all middleware, routes, and configuration.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config import get_settings
from app.exceptions import register_exception_handlers
from app.middleware.cors import setup_cors
from app.middleware.logging import LoggingMiddleware, setup_logging
from app.middleware.security import setup_security_headers

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown."""
    # Startup
    setup_logging(app)
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    description="Corporate Wellness & Fitness Compliance Platform API",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Middleware (order matters — last added is first executed)
setup_security_headers(app)
app.add_middleware(LoggingMiddleware)
setup_cors(app)

# Exception handlers
register_exception_handlers(app)

# Routes
app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
    }
