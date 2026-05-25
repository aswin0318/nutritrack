"""Event API routes."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user, require_manager
from app.models.user import User
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.services.event import EventService
from app.utils.pagination import PaginatedResponse

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=PaginatedResponse)
async def list_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List events in current organization."""
    service = EventService(db)
    skip = (page - 1) * page_size
    events, total = await service.get_org_events(
        current_user.organization_id, status=status, skip=skip, limit=page_size
    )
    items = [_to_response(e) for e in events]
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get event details."""
    service = EventService(db)
    event = await service.get_event(event_id)
    return _to_response(event)


@router.post("", response_model=EventResponse, status_code=201)
async def create_event(
    data: EventCreate,
    current_user: User = Depends(require_manager),
    db: AsyncSession = Depends(get_db),
):
    """Create a new event (Manager+)."""
    service = EventService(db)
    event = await service.create_event(
        data.model_dump(), current_user.id, current_user.organization_id
    )
    return _to_response(event)


@router.post("/{event_id}/register")
async def register_for_event(
    event_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Register for an event."""
    service = EventService(db)
    return await service.register_for_event(event_id, current_user.id)


def _to_response(e) -> EventResponse:
    return EventResponse(
        id=e.id, title=e.title, description=e.description, type=e.type,
        status=e.status, start_time=e.start_time, end_time=e.end_time,
        location=e.location, virtual_link=e.virtual_link, capacity=e.capacity,
        registered_count=e.registered_count, image_url=e.image_url,
        reward_points=e.reward_points, organization_id=e.organization_id,
        created_by=e.created_by,
        creator_name=e.creator.full_name if e.creator else None,
        created_at=e.created_at, updated_at=e.updated_at,
    )
