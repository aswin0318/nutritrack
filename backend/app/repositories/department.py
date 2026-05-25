"""Department repository."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department import Department
from app.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    """Repository for Department operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Department, db)
