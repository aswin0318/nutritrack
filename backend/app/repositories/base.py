"""Base repository with common CRUD operations."""

from typing import Any, Generic, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import Select, func, select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Generic repository implementing common CRUD operations."""

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: UUID) -> Optional[ModelType]:
        """Get a single record by ID."""
        query = select(self.model).where(self.model.id == id)
        if hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        filters: Optional[dict[str, Any]] = None,
    ) -> list[ModelType]:
        """Get all records with pagination, sorting, and filtering."""
        query = select(self.model)

        if hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted == False)

        # Apply filters
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    column = getattr(self.model, key)
                    if isinstance(value, str) and "%" in value:
                        query = query.where(column.ilike(value))
                    else:
                        query = query.where(column == value)

        # Apply sorting
        if hasattr(self.model, sort_by):
            order_column = getattr(self.model, sort_by)
            query = query.order_by(desc(order_column) if sort_order == "desc" else asc(order_column))

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count(self, filters: Optional[dict[str, Any]] = None) -> int:
        """Count records with optional filtering."""
        query = select(func.count(self.model.id))

        if hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted == False)

        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    column = getattr(self.model, key)
                    if isinstance(value, str) and "%" in value:
                        query = query.where(column.ilike(value))
                    else:
                        query = query.where(column == value)

        result = await self.db.execute(query)
        return result.scalar_one()

    async def create(self, obj_data: dict[str, Any]) -> ModelType:
        """Create a new record."""
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, id: UUID, obj_data: dict[str, Any]) -> Optional[ModelType]:
        """Update an existing record."""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None

        for key, value in obj_data.items():
            if value is not None and hasattr(db_obj, key):
                setattr(db_obj, key, value)

        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def soft_delete(self, id: UUID) -> bool:
        """Soft delete a record."""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return False

        if hasattr(db_obj, "is_deleted"):
            db_obj.is_deleted = True
            from datetime import datetime, timezone
            db_obj.deleted_at = datetime.now(timezone.utc)
            await self.db.flush()
            return True
        return False

    async def hard_delete(self, id: UUID) -> bool:
        """Permanently delete a record."""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return False

        await self.db.delete(db_obj)
        await self.db.flush()
        return True
