"""Activity repository."""

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import ActivityLog
from app.repositories.base import BaseRepository


class ActivityRepository(BaseRepository[ActivityLog]):
    """Repository for ActivityLog operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(ActivityLog, db)

    async def get_user_activities(
        self,
        user_id: UUID,
        start_date: date | None = None,
        end_date: date | None = None,
        activity_type: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[ActivityLog]:
        query = select(ActivityLog).where(ActivityLog.user_id == user_id)

        if start_date:
            query = query.where(ActivityLog.activity_date >= start_date)
        if end_date:
            query = query.where(ActivityLog.activity_date <= end_date)
        if activity_type:
            query = query.where(ActivityLog.activity_type == activity_type)

        query = query.order_by(ActivityLog.activity_date.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_user_stats(self, user_id: UUID) -> dict:
        """Get aggregate activity statistics for a user."""
        total = await self.db.execute(
            select(func.count(ActivityLog.id)).where(ActivityLog.user_id == user_id)
        )
        total_steps = await self.db.execute(
            select(func.coalesce(func.sum(ActivityLog.value), 0)).where(
                ActivityLog.user_id == user_id, ActivityLog.activity_type == "steps"
            )
        )
        total_exercise = await self.db.execute(
            select(func.coalesce(func.sum(ActivityLog.duration_minutes), 0)).where(
                ActivityLog.user_id == user_id, ActivityLog.activity_type == "exercise"
            )
        )
        total_calories = await self.db.execute(
            select(func.coalesce(func.sum(ActivityLog.calories_burned), 0)).where(
                ActivityLog.user_id == user_id
            )
        )
        total_points = await self.db.execute(
            select(func.coalesce(func.sum(ActivityLog.points_earned), 0)).where(
                ActivityLog.user_id == user_id
            )
        )

        return {
            "total_activities": total.scalar_one(),
            "total_steps": int(total_steps.scalar_one()),
            "total_exercise_minutes": int(total_exercise.scalar_one()),
            "total_calories_burned": int(total_calories.scalar_one()),
            "total_points_earned": int(total_points.scalar_one()),
        }
