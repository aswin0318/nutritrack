"""User model with RBAC support."""

import uuid
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, SoftDeleteMixin


class Role(BaseModel):
    """Role entity for RBAC."""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    users = relationship("User", back_populates="role", lazy="selectin")
    permissions = relationship("RolePermission", back_populates="role", lazy="selectin")


class Permission(BaseModel):
    """Permission entity."""

    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    resource: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    roles = relationship("RolePermission", back_populates="permission", lazy="selectin")


class RolePermission(BaseModel):
    """Many-to-many relationship between roles and permissions."""

    __tablename__ = "role_permissions"

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


class User(BaseModel, SoftDeleteMixin):
    """User entity - core identity model."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    employee_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)

    # Scores
    wellness_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reward_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Foreign keys
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False
    )

    # Relationships
    organization = relationship("Organization", back_populates="users")
    department = relationship("Department", back_populates="users", foreign_keys=[department_id])
    role = relationship("Role", back_populates="users")
    activities = relationship("ActivityLog", back_populates="user", lazy="selectin")
    wellness_goals = relationship("WellnessGoal", back_populates="user", lazy="selectin")
    challenge_participations = relationship("ChallengeParticipation", back_populates="user", lazy="selectin")
    event_registrations = relationship("EventRegistration", back_populates="user", lazy="selectin")
    user_rewards = relationship("UserReward", back_populates="user", lazy="selectin")
    notifications = relationship("Notification", back_populates="user", lazy="selectin")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
