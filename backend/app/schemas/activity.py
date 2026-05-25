"""Pydantic schemas for activity tracking."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ActivityLogCreate(BaseModel):
    activity_type: str = Field(..., max_length=50)
    activity_date: date
    value: float = Field(..., ge=0)
    unit: str = Field(..., max_length=30)
    duration_minutes: Optional[int] = Field(None, ge=0)
    calories_burned: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None


class ActivityLogResponse(BaseModel):
    id: UUID
    activity_type: str
    activity_date: date
    value: float
    unit: str
    duration_minutes: Optional[int] = None
    calories_burned: Optional[int] = None
    notes: Optional[str] = None
    points_earned: int
    user_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class ActivitySummary(BaseModel):
    total_activities: int
    total_steps: int
    total_exercise_minutes: int
    total_calories_burned: int
    total_points_earned: int
    streak_days: int
    activities_this_week: int
    activities_this_month: int
