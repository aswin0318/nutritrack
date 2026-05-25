"""Event and registration models."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, SoftDeleteMixin


class Event(BaseModel, SoftDeleteMixin):
    """Corporate fitness or wellness event."""

    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # workshop, seminar, fitness_class, health_screening, webinar
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="upcoming", index=True)  # upcoming, ongoing, completed, cancelled
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    virtual_link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    registered_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    reward_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Foreign keys
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    organization = relationship("Organization", back_populates="events")
    creator = relationship("User", foreign_keys=[created_by], lazy="selectin")
    registrations = relationship("EventRegistration", back_populates="event", lazy="selectin")


class EventRegistration(BaseModel):
    """User registration for an event."""

    __tablename__ = "event_registrations"

    status: Mapped[str] = mapped_column(String(30), nullable=False, default="registered")  # registered, attended, cancelled, no_show
    attended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="event_registrations")
    event = relationship("Event", back_populates="registrations")
