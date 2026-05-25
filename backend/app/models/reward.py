"""Reward, achievement, and user reward models."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, SoftDeleteMixin


class Reward(BaseModel, SoftDeleteMixin):
    """Reward catalog item."""

    __tablename__ = "rewards"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # merchandise, experience, donation, gift_card
    points_required: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity_available: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Foreign keys
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    organization = relationship("Organization", back_populates="rewards")
    user_rewards = relationship("UserReward", back_populates="reward", lazy="selectin")


class UserReward(BaseModel):
    """Record of a user earning or redeeming a reward."""

    __tablename__ = "user_rewards"

    type: Mapped[str] = mapped_column(String(30), nullable=False)  # earned, redeemed
    points: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="completed")  # pending, completed, cancelled

    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    reward_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rewards.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    user = relationship("User", back_populates="user_rewards")
    reward = relationship("Reward", back_populates="user_rewards")


class Achievement(BaseModel):
    """Achievement badge definition."""

    __tablename__ = "achievements"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # fitness, nutrition, consistency, social
    criteria_type: Mapped[str] = mapped_column(String(50), nullable=False)  # challenge_count, streak_days, points_earned
    criteria_value: Mapped[int] = mapped_column(Integer, nullable=False)
    points_reward: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement", lazy="selectin")


class UserAchievement(BaseModel):
    """Record of a user unlocking an achievement."""

    __tablename__ = "user_achievements"

    unlocked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    achievement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    user = relationship("User", lazy="selectin")
    achievement = relationship("Achievement", back_populates="user_achievements")
