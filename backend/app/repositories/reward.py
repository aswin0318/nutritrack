"""Reward repository."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reward import Reward, UserReward
from app.repositories.base import BaseRepository


class RewardRepository(BaseRepository[Reward]):
    """Repository for Reward operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Reward, db)

    async def get_by_organization(
        self,
        organization_id: UUID,
        category: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Reward]:
        query = (
            select(Reward)
            .where(Reward.organization_id == organization_id, Reward.is_deleted == False, Reward.is_active == True)
        )
        if category:
            query = query.where(Reward.category == category)
        query = query.order_by(Reward.points_required.asc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_user_reward(self, data: dict) -> UserReward:
        user_reward = UserReward(**data)
        self.db.add(user_reward)
        await self.db.flush()
        await self.db.refresh(user_reward)
        return user_reward

    async def get_user_rewards(self, user_id: UUID, skip: int = 0, limit: int = 20) -> list[UserReward]:
        query = (
            select(UserReward)
            .where(UserReward.user_id == user_id)
            .order_by(UserReward.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_user_total_earned(self, user_id: UUID) -> int:
        query = select(func.coalesce(func.sum(UserReward.points), 0)).where(
            UserReward.user_id == user_id, UserReward.type == "earned"
        )
        result = await self.db.execute(query)
        return result.scalar_one()

    async def get_user_total_redeemed(self, user_id: UUID) -> int:
        query = select(func.coalesce(func.sum(UserReward.points), 0)).where(
            UserReward.user_id == user_id, UserReward.type == "redeemed"
        )
        result = await self.db.execute(query)
        return result.scalar_one()
