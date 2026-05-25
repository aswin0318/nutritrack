"""Reward API routes."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user, require_hr_admin
from app.models.user import User
from app.schemas.reward import PointsSummary, RewardCreate, RewardResponse
from app.services.reward import RewardService

router = APIRouter(prefix="/rewards", tags=["Rewards"])


@router.get("", response_model=list[RewardResponse])
async def list_rewards(
    category: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List available rewards."""
    service = RewardService(db)
    rewards = await service.get_catalog(current_user.organization_id, category=category)
    return [RewardResponse.model_validate(r) for r in rewards]


@router.post("/{reward_id}/redeem")
async def redeem_reward(
    reward_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Redeem a reward."""
    service = RewardService(db)
    return await service.redeem_reward(reward_id, current_user.id)


@router.get("/points/summary", response_model=PointsSummary)
async def get_points_summary(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's points summary."""
    service = RewardService(db)
    return await service.get_points_summary(current_user.id)
