"""Analytics service for HR dashboards."""

from uuid import UUID

from sqlalchemy import func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    User, Challenge, ChallengeParticipation, Event, EventRegistration,
    ActivityLog, Department
)


class AnalyticsService:
    """Service for HR analytics and dashboard data."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_stats(self, org_id: UUID) -> dict:
        """Get top-level dashboard statistics."""
        total_users = await self._count(User, User.organization_id == org_id)
        active_users = await self._count(User, and_(User.organization_id == org_id, User.is_active == True))
        total_challenges = await self._count(Challenge, Challenge.organization_id == org_id)
        active_challenges = await self._count(
            Challenge, and_(Challenge.organization_id == org_id, Challenge.status == "active")
        )
        total_events = await self._count(Event, Event.organization_id == org_id)
        total_departments = await self._count(Department, Department.organization_id == org_id)

        # Average wellness score
        avg_result = await self.db.execute(
            select(func.coalesce(func.avg(User.wellness_score), 0))
            .where(User.organization_id == org_id, User.is_active == True)
        )
        avg_wellness = round(float(avg_result.scalar_one()), 1)

        return {
            "total_employees": total_users,
            "active_employees": active_users,
            "total_challenges": total_challenges,
            "active_challenges": active_challenges,
            "total_events": total_events,
            "total_departments": total_departments,
            "avg_wellness_score": avg_wellness,
            "participation_rate": round((active_users / total_users * 100) if total_users > 0 else 0, 1),
        }

    async def get_participation_trends(self, org_id: UUID) -> list[dict]:
        """Get monthly participation trends."""
        # Activity counts by month
        query = (
            select(
                func.date_trunc("month", ActivityLog.created_at).label("month"),
                func.count(func.distinct(ActivityLog.user_id)).label("active_users"),
                func.count(ActivityLog.id).label("total_activities"),
            )
            .join(User, ActivityLog.user_id == User.id)
            .where(User.organization_id == org_id)
            .group_by(func.date_trunc("month", ActivityLog.created_at))
            .order_by(func.date_trunc("month", ActivityLog.created_at).desc())
            .limit(12)
        )
        result = await self.db.execute(query)
        rows = result.all()

        return [
            {
                "month": str(row.month.strftime("%Y-%m")) if row.month else "",
                "active_users": row.active_users,
                "total_activities": row.total_activities,
            }
            for row in rows
        ]

    async def get_department_engagement(self, org_id: UUID) -> list[dict]:
        """Get engagement metrics by department."""
        query = (
            select(
                Department.name.label("department"),
                func.count(func.distinct(User.id)).label("total_employees"),
                func.coalesce(func.avg(User.wellness_score), 0).label("avg_wellness"),
                func.count(func.distinct(ChallengeParticipation.id)).label("challenge_participations"),
            )
            .outerjoin(User, and_(User.department_id == Department.id, User.is_deleted == False))
            .outerjoin(ChallengeParticipation, ChallengeParticipation.user_id == User.id)
            .where(Department.organization_id == org_id)
            .group_by(Department.id, Department.name)
        )
        result = await self.db.execute(query)
        rows = result.all()

        return [
            {
                "department": row.department,
                "total_employees": row.total_employees,
                "avg_wellness_score": round(float(row.avg_wellness), 1),
                "challenge_participations": row.challenge_participations,
            }
            for row in rows
        ]

    async def get_challenge_completion_rates(self, org_id: UUID) -> dict:
        """Get challenge completion statistics."""
        total_participations = await self.db.execute(
            select(func.count(ChallengeParticipation.id))
            .join(Challenge, ChallengeParticipation.challenge_id == Challenge.id)
            .where(Challenge.organization_id == org_id)
        )
        completed = await self.db.execute(
            select(func.count(ChallengeParticipation.id))
            .join(Challenge, ChallengeParticipation.challenge_id == Challenge.id)
            .where(Challenge.organization_id == org_id, ChallengeParticipation.status == "completed")
        )

        total = total_participations.scalar_one()
        done = completed.scalar_one()

        return {
            "total_participations": total,
            "completed": done,
            "completion_rate": round((done / total * 100) if total > 0 else 0, 1),
        }

    async def _count(self, model, *conditions) -> int:
        query = select(func.count(model.id))
        if hasattr(model, "is_deleted"):
            query = query.where(model.is_deleted == False)
        for cond in conditions:
            query = query.where(cond)
        result = await self.db.execute(query)
        return result.scalar_one()
