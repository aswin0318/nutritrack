"""Challenge service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BadRequestException, ConflictException, NotFoundException
from app.models.challenge import Challenge
from app.repositories.challenge import ChallengeRepository
from app.schemas.challenge import ChallengeCreate, ChallengeUpdate, LeaderboardEntry


class ChallengeService:
    """Service for challenge operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.challenge_repo = ChallengeRepository(db)

    async def create_challenge(self, data: ChallengeCreate, user_id: UUID, org_id: UUID) -> Challenge:
        challenge_data = data.model_dump()
        challenge_data["organization_id"] = org_id
        challenge_data["created_by"] = user_id
        challenge_data["status"] = "draft"
        return await self.challenge_repo.create(challenge_data)

    async def get_challenge(self, challenge_id: UUID) -> Challenge:
        challenge = await self.challenge_repo.get_by_id(challenge_id)
        if not challenge:
            raise NotFoundException("Challenge", str(challenge_id))
        return challenge

    async def update_challenge(self, challenge_id: UUID, data: ChallengeUpdate) -> Challenge:
        update_data = data.model_dump(exclude_unset=True)
        challenge = await self.challenge_repo.update(challenge_id, update_data)
        if not challenge:
            raise NotFoundException("Challenge", str(challenge_id))
        return challenge

    async def get_org_challenges(
        self, org_id: UUID, status: str | None = None, skip: int = 0, limit: int = 20
    ) -> tuple[list[Challenge], int]:
        challenges = await self.challenge_repo.get_by_organization(
            org_id, status=status, skip=skip, limit=limit
        )
        total = await self.challenge_repo.count({"organization_id": org_id})
        return challenges, total

    async def join_challenge(self, challenge_id: UUID, user_id: UUID) -> dict:
        challenge = await self.get_challenge(challenge_id)

        if challenge.status != "active":
            raise BadRequestException("Challenge is not active")

        existing = await self.challenge_repo.get_participation(user_id, challenge_id)
        if existing:
            raise ConflictException("Already joined this challenge")

        if challenge.max_participants:
            count = await self.challenge_repo.count_participants(challenge_id)
            if count >= challenge.max_participants:
                raise BadRequestException("Challenge is full")

        participation = await self.challenge_repo.create_participation({
            "user_id": user_id,
            "challenge_id": challenge_id,
            "progress_value": 0.0,
            "status": "active",
        })

        return {"message": "Successfully joined the challenge", "participation_id": str(participation.id)}

    async def get_leaderboard(self, challenge_id: UUID) -> list[LeaderboardEntry]:
        challenge = await self.get_challenge(challenge_id)
        participations = await self.challenge_repo.get_leaderboard(challenge_id)

        leaderboard = []
        for rank, p in enumerate(participations, 1):
            progress_pct = (p.progress_value / challenge.target_value * 100) if challenge.target_value > 0 else 0
            leaderboard.append(LeaderboardEntry(
                rank=rank,
                user_id=p.user_id,
                user_name=p.user.full_name if p.user else "Unknown",
                department_name=p.user.department.name if p.user and p.user.department else None,
                progress_value=p.progress_value,
                progress_percentage=min(100, progress_pct),
                points_earned=p.points_earned,
            ))

        return leaderboard
