"""Analytics API routes for HR dashboard."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_hr_admin
from app.models.user import User
from app.services.analytics import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: User = Depends(require_hr_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get top-level dashboard statistics (HR Admin+)."""
    service = AnalyticsService(db)
    return await service.get_dashboard_stats(current_user.organization_id)


@router.get("/participation")
async def get_participation_trends(
    current_user: User = Depends(require_hr_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get monthly participation trends (HR Admin+)."""
    service = AnalyticsService(db)
    return await service.get_participation_trends(current_user.organization_id)


@router.get("/departments")
async def get_department_engagement(
    current_user: User = Depends(require_hr_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get department engagement metrics (HR Admin+)."""
    service = AnalyticsService(db)
    return await service.get_department_engagement(current_user.organization_id)


@router.get("/challenges/completion")
async def get_challenge_completion(
    current_user: User = Depends(require_hr_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get challenge completion rates (HR Admin+)."""
    service = AnalyticsService(db)
    return await service.get_challenge_completion_rates(current_user.organization_id)
