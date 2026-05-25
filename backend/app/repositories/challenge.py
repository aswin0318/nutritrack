"""Challenge repository."""

from typing import Optional
from uuid import UUID

from sqlalchemy import func, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.challenge import Challenge, ChallengeParticipation
from app.repositories.base import BaseRepository


class ChallengeRepository(BaseRepository[Challenge]):
    """Repository for Challenge operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Challenge, db)

    async def get_by_organization(
        self,
        organization_id: UUID,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Challenge]:
        query = (
            select(Challenge)
            .where(Challenge.organization_id == organization_id, Challenge.is_deleted == False)
        )
        if status:
            query = query.where(Challenge.status == status)
        query = query.order_by(Challenge.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_participation(
        self, user_id: UUID, challenge_id: UUID
    ) -> Optional[ChallengeParticipation]:
        query = select(ChallengeParticipation).where(
            ChallengeParticipation.user_id == user_id,
            ChallengeParticipation.challenge_id == challenge_id,
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_participation(self, data: dict) -> ChallengeParticipation:
        participation = ChallengeParticipation(**data)
        self.db.add(participation)
        await self.db.flush()
        await self.db.refresh(participation)
        return participation

    async def get_leaderboard(self, challenge_id: UUID, limit: int = 50) -> list[ChallengeParticipation]:
        query = (
            select(ChallengeParticipation)
            .options(selectinload(ChallengeParticipation.user))
            .where(ChallengeParticipation.challenge_id == challenge_id)
            .order_by(desc(ChallengeParticipation.progress_value))
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_participants(self, challenge_id: UUID) -> int:
        query = select(func.count(ChallengeParticipation.id)).where(
            ChallengeParticipation.challenge_id == challenge_id
        )
        result = await self.db.execute(query)
        return result.scalar_one()

    async def get_user_participations(self, user_id: UUID) -> list[ChallengeParticipation]:
        query = (
            select(ChallengeParticipation)
            .options(selectinload(ChallengeParticipation.challenge))
            .where(ChallengeParticipation.user_id == user_id)
            .order_by(ChallengeParticipation.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
