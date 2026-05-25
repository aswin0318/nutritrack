"""Activity API routes."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.activity import ActivityLogCreate, ActivityLogResponse, ActivitySummary
from app.services.activity import ActivityService

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.post("", response_model=ActivityLogResponse, status_code=201)
async def log_activity(
    data: ActivityLogCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Log a new activity."""
    service = ActivityService(db)
    activity = await service.log_activity(data, current_user.id)
    return ActivityLogResponse.model_validate(activity)


@router.get("", response_model=list[ActivityLogResponse])
async def list_activities(
    activity_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List current user's activities."""
    service = ActivityService(db)
    skip = (page - 1) * page_size
    activities = await service.get_user_activities(
        current_user.id, skip=skip, limit=page_size, activity_type=activity_type
    )
    return [ActivityLogResponse.model_validate(a) for a in activities]


@router.get("/summary", response_model=ActivitySummary)
async def get_activity_summary(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get activity summary for current user."""
    service = ActivityService(db)
    return await service.get_activity_summary(current_user.id)
