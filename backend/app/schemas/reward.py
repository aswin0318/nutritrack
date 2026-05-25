"""Pydantic schemas for rewards."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class RewardBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    category: str = Field(..., max_length=50)
    points_required: int = Field(..., ge=0)
    quantity_available: Optional[int] = Field(None, ge=0)


class RewardCreate(RewardBase):
    organization_id: Optional[UUID] = None


class RewardUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    points_required: Optional[int] = Field(None, ge=0)
    quantity_available: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class RewardResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    category: str
    points_required: int
    quantity_available: Optional[int] = None
    image_url: Optional[str] = None
    is_active: bool
    organization_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RedeemRewardRequest(BaseModel):
    pass


class UserRewardResponse(BaseModel):
    id: UUID
    type: str
    points: int
    description: Optional[str] = None
    status: str
    reward_name: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PointsSummary(BaseModel):
    total_earned: int
    total_redeemed: int
    current_balance: int
    this_month_earned: int
