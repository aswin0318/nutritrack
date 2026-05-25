"""Pydantic schemas for events."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    type: str = Field(..., max_length=50)
    start_time: datetime
    end_time: datetime
    location: Optional[str] = Field(None, max_length=500)
    virtual_link: Optional[str] = Field(None, max_length=500)
    capacity: Optional[int] = Field(None, ge=1)
    reward_points: int = Field(0, ge=0)


class EventCreate(EventBase):
    organization_id: Optional[UUID] = None


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = Field(None, max_length=30)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=500)
    virtual_link: Optional[str] = Field(None, max_length=500)
    capacity: Optional[int] = Field(None, ge=1)


class EventResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    type: str
    status: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    virtual_link: Optional[str] = None
    capacity: Optional[int] = None
    registered_count: int
    image_url: Optional[str] = None
    reward_points: int
    organization_id: UUID
    created_by: Optional[UUID] = None
    creator_name: Optional[str] = None
    is_registered: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EventRegistrationRequest(BaseModel):
    pass


class EventRegistrationResponse(BaseModel):
    id: UUID
    user_id: UUID
    user_name: str = ""
    event_id: UUID
    status: str
    attended_at: Optional[datetime] = None
    feedback: Optional[str] = None
    rating: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}
