"""Services for organization, department, and notifications."""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.organization import OrganizationRepository
from app.repositories.department import DepartmentRepository
from app.exceptions import NotFoundException


class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.repo = OrganizationRepository(db)

    async def get(self, id: UUID):
        org = await self.repo.get_by_id(id)
        if not org:
            raise NotFoundException("Organization", str(id))
        return org

    async def list_all(self, skip: int = 0, limit: int = 20):
        return await self.repo.get_all(skip=skip, limit=limit)

    async def create(self, data: dict):
        return await self.repo.create(data)

    async def update(self, id: UUID, data: dict):
        org = await self.repo.update(id, data)
        if not org:
            raise NotFoundException("Organization", str(id))
        return org


class DepartmentService:
    def __init__(self, db: AsyncSession):
        self.repo = DepartmentRepository(db)

    async def get(self, id: UUID):
        dept = await self.repo.get_by_id(id)
        if not dept:
            raise NotFoundException("Department", str(id))
        return dept

    async def list_by_org(self, org_id: UUID, skip: int = 0, limit: int = 20):
        return await self.repo.get_all(
            skip=skip, limit=limit, filters={"organization_id": org_id}
        )

    async def count_by_org(self, org_id: UUID) -> int:
        return await self.repo.count({"organization_id": org_id})

    async def create(self, data: dict):
        return await self.repo.create(data)

    async def update(self, id: UUID, data: dict):
        dept = await self.repo.update(id, data)
        if not dept:
            raise NotFoundException("Department", str(id))
        return dept

    async def delete(self, id: UUID):
        return await self.repo.soft_delete(id)


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_notification(self, user_id: UUID, title: str, message: str, type: str = "system"):
        from app.models.notification import Notification
        notif = Notification(
            user_id=user_id, title=title, message=message, type=type
        )
        self.db.add(notif)
        await self.db.flush()
        return notif

    async def get_user_notifications(self, user_id: UUID, skip: int = 0, limit: int = 20):
        from sqlalchemy import select
        from app.models.notification import Notification
        query = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .offset(skip).limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def mark_as_read(self, notification_id: UUID):
        from sqlalchemy import select
        from app.models.notification import Notification
        query = select(Notification).where(Notification.id == notification_id)
        result = await self.db.execute(query)
        notif = result.scalar_one_or_none()
        if notif:
            notif.is_read = True
            await self.db.flush()
        return notif
