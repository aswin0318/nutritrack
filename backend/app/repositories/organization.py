"""Organization repository."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization
from app.repositories.base import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    """Repository for Organization operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Organization, db)
