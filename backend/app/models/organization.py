"""Organization model."""

import uuid
from typing import Optional

from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, SoftDeleteMixin


class Organization(BaseModel, SoftDeleteMixin):
    """Organization entity - top-level tenant."""

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    domain: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    size_tier: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # small, medium, large, enterprise
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    departments = relationship("Department", back_populates="organization", lazy="selectin")
    users = relationship("User", back_populates="organization", lazy="selectin")
    challenges = relationship("Challenge", back_populates="organization", lazy="selectin")
    events = relationship("Event", back_populates="organization", lazy="selectin")
    wellness_programs = relationship("WellnessProgram", back_populates="organization", lazy="selectin")
    rewards = relationship("Reward", back_populates="organization", lazy="selectin")
