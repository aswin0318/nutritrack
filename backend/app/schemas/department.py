"""Pydantic schemas for departments."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=20)
    description: Optional[str] = Field(None, max_length=500)


class DepartmentCreate(DepartmentBase):
    organization_id: UUID
    manager_id: Optional[UUID] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, max_length=500)
    manager_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class DepartmentResponse(BaseModel):
    id: UUID
    name: str
    code: str
    description: Optional[str] = None
    is_active: bool
    organization_id: UUID
    manager_id: Optional[UUID] = None
    manager_name: Optional[str] = None
    employee_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
