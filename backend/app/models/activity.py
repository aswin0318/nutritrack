"""Activity tracking model."""

import uuid
from datetime import date
from typing import Optional

from sqlalchemy import Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ActivityLog(BaseModel):
    """Daily activity log entry for a user."""

    __tablename__ = "activity_logs"

    activity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # steps, exercise, meditation, nutrition, sleep
    activity_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)  # steps, minutes, hours, calories
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    calories_burned: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    points_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Relationships
    user = relationship("User", back_populates="activities")
