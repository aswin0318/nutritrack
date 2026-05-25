"""Pydantic schemas for users."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    employee_id: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    title: Optional[str] = Field(None, max_length=150)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    organization_id: UUID
    department_id: Optional[UUID] = None
    role_id: UUID


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    title: Optional[str] = Field(None, max_length=150)
    department_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    employee_id: Optional[str] = None
    phone: Optional[str] = None
    title: Optional[str] = None
    avatar_url: Optional[str] = None
    wellness_score: int
    reward_points: int
    is_active: bool
    organization_id: UUID
    department_id: Optional[UUID] = None
    role_id: UUID
    role_name: Optional[str] = None
    department_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserProfileResponse(UserResponse):
    organization_name: Optional[str] = None
    challenges_completed: int = 0
    events_attended: int = 0
    goals_active: int = 0
