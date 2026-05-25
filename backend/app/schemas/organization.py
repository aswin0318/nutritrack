"""Pydantic schemas for organizations."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class OrganizationBase(BaseModel):
    name: str = Field(..., max_length=255)
    domain: Optional[str] = Field(None, max_length=255)
    industry: Optional[str] = Field(None, max_length=100)
    size_tier: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    domain: Optional[str] = Field(None, max_length=255)
    industry: Optional[str] = Field(None, max_length=100)
    size_tier: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    settings: Optional[dict] = None


class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    size_tier: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: bool
    settings: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    total_employees: int = 0
    total_departments: int = 0

    model_config = {"from_attributes": True}
