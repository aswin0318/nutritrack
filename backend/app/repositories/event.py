"""Event repository."""

from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event, EventRegistration
from app.repositories.base import BaseRepository


class EventRepository(BaseRepository[Event]):
    """Repository for Event operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Event, db)

    async def get_by_organization(
        self,
        organization_id: UUID,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Event]:
        query = (
            select(Event)
            .where(Event.organization_id == organization_id, Event.is_deleted == False)
        )
        if status:
            query = query.where(Event.status == status)
        query = query.order_by(Event.start_time.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_registration(
        self, user_id: UUID, event_id: UUID
    ) -> Optional[EventRegistration]:
        query = select(EventRegistration).where(
            EventRegistration.user_id == user_id,
            EventRegistration.event_id == event_id,
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_registration(self, data: dict) -> EventRegistration:
        registration = EventRegistration(**data)
        self.db.add(registration)
        await self.db.flush()
        await self.db.refresh(registration)
        return registration

    async def count_registrations(self, event_id: UUID) -> int:
        query = select(func.count(EventRegistration.id)).where(
            EventRegistration.event_id == event_id
        )
        result = await self.db.execute(query)
        return result.scalar_one()

    async def get_user_registrations(self, user_id: UUID) -> list[EventRegistration]:
        from sqlalchemy.orm import selectinload
        query = (
            select(EventRegistration)
            .options(selectinload(EventRegistration.event))
            .where(EventRegistration.user_id == user_id)
            .order_by(EventRegistration.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
