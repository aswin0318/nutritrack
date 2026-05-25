"""Challenge and participation models."""

import uuid
from datetime import date
from typing import Optional

from sqlalchemy import Boolean, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, SoftDeleteMixin


class Challenge(BaseModel, SoftDeleteMixin):
    """Team or individual wellness challenge."""

    __tablename__ = "challenges"

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # steps, exercise, nutrition, mindfulness, custom
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)  # draft, active, completed, cancelled
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    target_value: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    metric_unit: Mapped[str] = mapped_column(String(50), nullable=False, default="steps")
    reward_points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_participants: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_team_challenge: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Foreign keys
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    organization = relationship("Organization", back_populates="challenges")
    creator = relationship("User", foreign_keys=[created_by], lazy="selectin")
    participations = relationship("ChallengeParticipation", back_populates="challenge", lazy="selectin")


class ChallengeParticipation(BaseModel):
    """User participation in a challenge."""

    __tablename__ = "challenge_participations"

    progress_value: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")  # active, completed, withdrawn
    completed_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    points_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    challenge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="challenge_participations")
    challenge = relationship("Challenge", back_populates="participations")
