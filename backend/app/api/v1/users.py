"""User API routes."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user, require_hr_admin
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserProfileResponse
from app.services.user import UserService
from app.utils.pagination import PaginatedResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's profile."""
    service = UserService(db)
    user = await service.get_user(current_user.id)
    return UserProfileResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        employee_id=user.employee_id,
        phone=user.phone,
        title=user.title,
        avatar_url=user.avatar_url,
        wellness_score=user.wellness_score,
        reward_points=user.reward_points,
        is_active=user.is_active,
        organization_id=user.organization_id,
        department_id=user.department_id,
        role_id=user.role_id,
        role_name=user.role.name if user.role else None,
        department_name=user.department.name if user.department else None,
        organization_name=user.organization.name if user.organization else None,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user's profile."""
    service = UserService(db)
    user = await service.update_user(current_user.id, data)
    return _to_response(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a user by ID."""
    service = UserService(db)
    user = await service.get_user(user_id)
    return _to_response(user)


@router.get("", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    current_user: User = Depends(require_hr_admin),
    db: AsyncSession = Depends(get_db),
):
    """List users in current organization (HR Admin+)."""
    service = UserService(db)
    skip = (page - 1) * page_size
    users, total = await service.get_organization_users(
        current_user.organization_id, skip=skip, limit=page_size, search=search
    )
    return PaginatedResponse.create(
        items=[_to_response(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
    )


def _to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        employee_id=user.employee_id,
        phone=user.phone,
        title=user.title,
        avatar_url=user.avatar_url,
        wellness_score=user.wellness_score,
        reward_points=user.reward_points,
        is_active=user.is_active,
        organization_id=user.organization_id,
        department_id=user.department_id,
        role_id=user.role_id,
        role_name=user.role.name if user.role else None,
        department_name=user.department.name if user.department else None,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
