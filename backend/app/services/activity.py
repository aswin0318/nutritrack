"""Activity service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.activity import ActivityRepository
from app.repositories.user import UserRepository
from app.schemas.activity import ActivityLogCreate, ActivitySummary


ACTIVITY_POINTS = {
    "steps": 1,      # per 1000 steps
    "exercise": 5,   # per 30 minutes
    "meditation": 3, # per session
    "nutrition": 2,  # per log
    "sleep": 2,      # per log
}


class ActivityService:
    """Service for activity tracking."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.activity_repo = ActivityRepository(db)
        self.user_repo = UserRepository(db)

    async def log_activity(self, data: ActivityLogCreate, user_id: UUID):
        points = self._calculate_points(data.activity_type, data.value)

        activity = await self.activity_repo.create({
            **data.model_dump(),
            "user_id": user_id,
            "points_earned": points,
        })

        # Update user's reward points
        user = await self.user_repo.get_by_id(user_id)
        if user:
            await self.user_repo.update(user_id, {
                "reward_points": user.reward_points + points,
            })

        return activity

    async def get_user_activities(
        self, user_id: UUID, skip: int = 0, limit: int = 20, activity_type: str | None = None
    ):
        return await self.activity_repo.get_user_activities(
            user_id, activity_type=activity_type, skip=skip, limit=limit
        )

    async def get_activity_summary(self, user_id: UUID) -> ActivitySummary:
        stats = await self.activity_repo.get_user_stats(user_id)
        return ActivitySummary(
            **stats,
            streak_days=0,
            activities_this_week=0,
            activities_this_month=0,
        )

    def _calculate_points(self, activity_type: str, value: float) -> int:
        base = ACTIVITY_POINTS.get(activity_type, 1)
        if activity_type == "steps":
            return int(value / 1000) * base
        elif activity_type == "exercise":
            return int(value / 30) * base
        return base
