"""Pydantic schemas for challenges."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ChallengeBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    type: str = Field(..., max_length=50)
    start_date: date
    end_date: date
    target_value: int = Field(..., ge=0)
    metric_unit: str = Field(..., max_length=50)
    reward_points: int = Field(0, ge=0)
    max_participants: Optional[int] = Field(None, ge=1)
    is_team_challenge: bool = False


class ChallengeCreate(ChallengeBase):
    organization_id: Optional[UUID] = None


class ChallengeUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = Field(None, max_length=30)
    end_date: Optional[date] = None
    target_value: Optional[int] = Field(None, ge=0)
    reward_points: Optional[int] = Field(None, ge=0)
    max_participants: Optional[int] = Field(None, ge=1)


class ChallengeResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    type: str
    status: str
    start_date: date
    end_date: date
    target_value: int
    metric_unit: str
    reward_points: int
    max_participants: Optional[int] = None
    is_team_challenge: bool
    image_url: Optional[str] = None
    organization_id: UUID
    created_by: Optional[UUID] = None
    creator_name: Optional[str] = None
    participant_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class JoinChallengeRequest(BaseModel):
    pass


class ChallengeParticipationResponse(BaseModel):
    id: UUID
    user_id: UUID
    user_name: str = ""
    challenge_id: UUID
    progress_value: float
    status: str
    completed_at: Optional[date] = None
    points_earned: int
    progress_percentage: float = 0.0
    created_at: datetime

    model_config = {"from_attributes": True}


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: UUID
    user_name: str
    department_name: Optional[str] = None
    progress_value: float
    progress_percentage: float
    points_earned: int
