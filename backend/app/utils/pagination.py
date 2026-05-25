"""Pagination utilities for API endpoints."""

from typing import Generic, TypeVar, Sequence
from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Query parameters for pagination."""
    page: int = 1
    page_size: int = 20
    sort_by: str = "created_at"
    sort_order: str = "desc"

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

    @classmethod
    def create(
        cls,
        items: Sequence,
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse":
        total_pages = max(1, (total + page_size - 1) // page_size)
        return cls(
            items=list(items),
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )
