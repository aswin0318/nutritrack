"""User repository."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Find a user by email address."""
        query = (
            select(User)
            .options(selectinload(User.role), selectinload(User.department))
            .where(User.email == email, User.is_deleted == False)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id_with_relations(self, id: UUID) -> Optional[User]:
        """Get user with eager-loaded relations."""
        query = (
            select(User)
            .options(
                selectinload(User.role),
                selectinload(User.department),
                selectinload(User.organization),
            )
            .where(User.id == id, User.is_deleted == False)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_organization(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
    ) -> list[User]:
        """Get users by organization with optional search."""
        query = (
            select(User)
            .options(selectinload(User.role), selectinload(User.department))
            .where(User.organization_id == organization_id, User.is_deleted == False)
        )

        if search:
            search_term = f"%{search}%"
            query = query.where(
                (User.first_name.ilike(search_term))
                | (User.last_name.ilike(search_term))
                | (User.email.ilike(search_term))
            )

        query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_by_organization(self, organization_id: UUID) -> int:
        """Count users in an organization."""
        from sqlalchemy import func
        query = (
            select(func.count(User.id))
            .where(User.organization_id == organization_id, User.is_deleted == False)
        )
        result = await self.db.execute(query)
        return result.scalar_one()
