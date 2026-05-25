"""Pydantic schemas for wellness goals."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class WellnessGoalCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    category: str = Field(..., max_length=50)
    target_value: float = Field(..., ge=0)
    unit: str = Field(..., max_length=30)
    start_date: date
    end_date: date


class WellnessGoalUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    current_value: Optional[float] = Field(None, ge=0)
    target_value: Optional[float] = Field(None, ge=0)
    status: Optional[str] = Field(None, max_length=30)


class WellnessGoalResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    category: str
    target_value: float
    current_value: float
    unit: str
    start_date: date
    end_date: date
    status: str
    progress_percentage: float = 0.0
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
