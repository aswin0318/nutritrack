"""Reward service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BadRequestException, NotFoundException
from app.repositories.reward import RewardRepository
from app.repositories.user import UserRepository
from app.schemas.reward import PointsSummary


class RewardService:
    """Service for reward operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.reward_repo = RewardRepository(db)
        self.user_repo = UserRepository(db)

    async def get_catalog(self, org_id: UUID, category: str | None = None, skip: int = 0, limit: int = 20):
        return await self.reward_repo.get_by_organization(org_id, category=category, skip=skip, limit=limit)

    async def redeem_reward(self, reward_id: UUID, user_id: UUID) -> dict:
        reward = await self.reward_repo.get_by_id(reward_id)
        if not reward:
            raise NotFoundException("Reward", str(reward_id))

        if not reward.is_active:
            raise BadRequestException("Reward is no longer available")

        if reward.quantity_available is not None and reward.quantity_available <= 0:
            raise BadRequestException("Reward is out of stock")

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", str(user_id))

        if user.reward_points < reward.points_required:
            raise BadRequestException(
                f"Insufficient points. Required: {reward.points_required}, Available: {user.reward_points}"
            )

        # Deduct points
        await self.user_repo.update(user_id, {
            "reward_points": user.reward_points - reward.points_required,
        })

        # Create redemption record
        await self.reward_repo.create_user_reward({
            "user_id": user_id,
            "reward_id": reward_id,
            "type": "redeemed",
            "points": reward.points_required,
            "description": f"Redeemed: {reward.name}",
            "status": "completed",
        })

        # Decrement quantity
        if reward.quantity_available is not None:
            await self.reward_repo.update(reward_id, {
                "quantity_available": reward.quantity_available - 1,
            })

        return {"message": f"Successfully redeemed: {reward.name}"}

    async def get_points_summary(self, user_id: UUID) -> PointsSummary:
        total_earned = await self.reward_repo.get_user_total_earned(user_id)
        total_redeemed = await self.reward_repo.get_user_total_redeemed(user_id)

        user = await self.user_repo.get_by_id(user_id)
        balance = user.reward_points if user else 0

        return PointsSummary(
            total_earned=total_earned,
            total_redeemed=total_redeemed,
            current_balance=balance,
            this_month_earned=0,  # Calculated from date-filtered query
        )
