"""Event service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BadRequestException, ConflictException, NotFoundException
from app.models.event import Event
from app.repositories.event import EventRepository


class EventService:
    """Service for event operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.event_repo = EventRepository(db)

    async def create_event(self, data: dict, user_id: UUID, org_id: UUID) -> Event:
        data["organization_id"] = org_id
        data["created_by"] = user_id
        data["status"] = "upcoming"
        return await self.event_repo.create(data)

    async def get_event(self, event_id: UUID) -> Event:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise NotFoundException("Event", str(event_id))
        return event

    async def get_org_events(
        self, org_id: UUID, status: str | None = None, skip: int = 0, limit: int = 20
    ) -> tuple[list[Event], int]:
        events = await self.event_repo.get_by_organization(
            org_id, status=status, skip=skip, limit=limit
        )
        total = await self.event_repo.count({"organization_id": org_id})
        return events, total

    async def register_for_event(self, event_id: UUID, user_id: UUID) -> dict:
        event = await self.get_event(event_id)

        if event.status not in ("upcoming", "ongoing"):
            raise BadRequestException("Event is not open for registration")

        existing = await self.event_repo.get_registration(user_id, event_id)
        if existing:
            raise ConflictException("Already registered for this event")

        if event.capacity and event.registered_count >= event.capacity:
            raise BadRequestException("Event is at full capacity")

        registration = await self.event_repo.create_registration({
            "user_id": user_id,
            "event_id": event_id,
            "status": "registered",
        })

        # Increment registered count
        await self.event_repo.update(event_id, {"registered_count": event.registered_count + 1})

        return {"message": "Successfully registered for the event", "registration_id": str(registration.id)}
