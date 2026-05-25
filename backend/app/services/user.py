"""User service."""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundException
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserResponse, UserUpdate


class UserService:
    """Service for user operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def get_user(self, user_id: UUID) -> User:
        user = await self.user_repo.get_by_id_with_relations(user_id)
        if not user:
            raise NotFoundException("User", str(user_id))
        return user

    async def update_user(self, user_id: UUID, data: UserUpdate) -> User:
        update_data = data.model_dump(exclude_unset=True)
        user = await self.user_repo.update(user_id, update_data)
        if not user:
            raise NotFoundException("User", str(user_id))
        return user

    async def get_organization_users(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
    ) -> tuple[list[User], int]:
        users = await self.user_repo.get_by_organization(
            organization_id, skip=skip, limit=limit, search=search
        )
        total = await self.user_repo.count_by_organization(organization_id)
        return users, total

    async def deactivate_user(self, user_id: UUID) -> User:
        user = await self.user_repo.update(user_id, {"is_active": False})
        if not user:
            raise NotFoundException("User", str(user_id))
        return user

    async def activate_user(self, user_id: UUID) -> User:
        user = await self.user_repo.update(user_id, {"is_active": True})
        if not user:
            raise NotFoundException("User", str(user_id))
        return user
