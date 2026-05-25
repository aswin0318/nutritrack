"""Models package - exports all models for Alembic and app usage."""

from app.models.base import Base, BaseModel, SoftDeleteMixin, TimestampMixin
from app.models.organization import Organization
from app.models.user import User, Role, Permission, RolePermission
from app.models.department import Department
from app.models.challenge import Challenge, ChallengeParticipation
from app.models.event import Event, EventRegistration
from app.models.reward import Reward, UserReward, Achievement, UserAchievement
from app.models.activity import ActivityLog
from app.models.wellness import WellnessProgram, WellnessGoal
from app.models.notification import Notification
from app.models.audit import AuditLog

__all__ = [
    "Base",
    "BaseModel",
    "TimestampMixin",
    "SoftDeleteMixin",
    "Organization",
    "User",
    "Role",
    "Permission",
    "RolePermission",
    "Department",
    "Challenge",
    "ChallengeParticipation",
    "Event",
    "EventRegistration",
    "Reward",
    "UserReward",
    "Achievement",
    "UserAchievement",
    "ActivityLog",
    "WellnessProgram",
    "WellnessGoal",
    "Notification",
    "AuditLog",
]
