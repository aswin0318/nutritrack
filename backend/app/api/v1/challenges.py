"""Challenge API routes."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user, require_manager
from app.models.user import User
from app.schemas.challenge import ChallengeCreate, ChallengeResponse, ChallengeUpdate, LeaderboardEntry
from app.services.challenge import ChallengeService
from app.utils.pagination import PaginatedResponse

router = APIRouter(prefix="/challenges", tags=["Challenges"])


@router.get("", response_model=PaginatedResponse)
async def list_challenges(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List challenges in current organization."""
    service = ChallengeService(db)
    skip = (page - 1) * page_size
    challenges, total = await service.get_org_challenges(
        current_user.organization_id, status=status, skip=skip, limit=page_size
    )
    items = []
    for c in challenges:
        items.append(ChallengeResponse(
            id=c.id, title=c.title, description=c.description, type=c.type,
            status=c.status, start_date=c.start_date, end_date=c.end_date,
            target_value=c.target_value, metric_unit=c.metric_unit,
            reward_points=c.reward_points, max_participants=c.max_participants,
            is_team_challenge=c.is_team_challenge, image_url=c.image_url,
            organization_id=c.organization_id, created_by=c.created_by,
            creator_name=c.creator.full_name if c.creator else None,
            participant_count=len(c.participations) if c.participations else 0,
            created_at=c.created_at, updated_at=c.updated_at,
        ))
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)


@router.get("/{challenge_id}", response_model=ChallengeResponse)
async def get_challenge(
    challenge_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get challenge details."""
    service = ChallengeService(db)
    c = await service.get_challenge(challenge_id)
    return ChallengeResponse(
        id=c.id, title=c.title, description=c.description, type=c.type,
        status=c.status, start_date=c.start_date, end_date=c.end_date,
        target_value=c.target_value, metric_unit=c.metric_unit,
        reward_points=c.reward_points, max_participants=c.max_participants,
        is_team_challenge=c.is_team_challenge, image_url=c.image_url,
        organization_id=c.organization_id, created_by=c.created_by,
        creator_name=c.creator.full_name if c.creator else None,
        participant_count=len(c.participations) if c.participations else 0,
        created_at=c.created_at, updated_at=c.updated_at,
    )


@router.post("", response_model=ChallengeResponse, status_code=201)
async def create_challenge(
    data: ChallengeCreate,
    current_user: User = Depends(require_manager),
    db: AsyncSession = Depends(get_db),
):
    """Create a new challenge (Manager+)."""
    service = ChallengeService(db)
    c = await service.create_challenge(data, current_user.id, current_user.organization_id)
    return ChallengeResponse(
        id=c.id, title=c.title, description=c.description, type=c.type,
        status=c.status, start_date=c.start_date, end_date=c.end_date,
        target_value=c.target_value, metric_unit=c.metric_unit,
        reward_points=c.reward_points, max_participants=c.max_participants,
        is_team_challenge=c.is_team_challenge, image_url=c.image_url,
        organization_id=c.organization_id, created_by=c.created_by,
        participant_count=0,
        created_at=c.created_at, updated_at=c.updated_at,
    )


@router.put("/{challenge_id}", response_model=ChallengeResponse)
async def update_challenge(
    challenge_id: UUID,
    data: ChallengeUpdate,
    current_user: User = Depends(require_manager),
    db: AsyncSession = Depends(get_db),
):
    """Update a challenge (Manager+)."""
    service = ChallengeService(db)
    c = await service.update_challenge(challenge_id, data)
    return ChallengeResponse(
        id=c.id, title=c.title, description=c.description, type=c.type,
        status=c.status, start_date=c.start_date, end_date=c.end_date,
        target_value=c.target_value, metric_unit=c.metric_unit,
        reward_points=c.reward_points, max_participants=c.max_participants,
        is_team_challenge=c.is_team_challenge, image_url=c.image_url,
        organization_id=c.organization_id, created_by=c.created_by,
        participant_count=len(c.participations) if c.participations else 0,
        created_at=c.created_at, updated_at=c.updated_at,
    )


@router.post("/{challenge_id}/join")
async def join_challenge(
    challenge_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Join a challenge."""
    service = ChallengeService(db)
    return await service.join_challenge(challenge_id, current_user.id)


@router.get("/{challenge_id}/leaderboard", response_model=list[LeaderboardEntry])
async def get_leaderboard(
    challenge_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get challenge leaderboard."""
    service = ChallengeService(db)
    return await service.get_leaderboard(challenge_id)
