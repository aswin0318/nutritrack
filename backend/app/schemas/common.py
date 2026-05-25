"""Common schemas used across the application."""

from typing import Any, Optional
from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    error: bool = True
    message: str
    detail: Optional[Any] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
