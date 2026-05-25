"""
FastAPI dependency injection for authentication and authorization.
"""

from typing import Optional
from uuid import UUID

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions import ForbiddenException, UnauthorizedException
from app.models.user import User
from app.utils.security import decode_token

security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extract and validate the current user from JWT token."""
    if not credentials:
        raise UnauthorizedException("Missing authentication token")

    try:
        payload = decode_token(credentials.credentials)
    except ValueError:
        raise UnauthorizedException("Invalid or expired token")

    if payload.get("type") != "access":
        raise UnauthorizedException("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload")

    result = await db.execute(
        select(User).where(User.id == UUID(user_id), User.is_active == True, User.is_deleted == False)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise UnauthorizedException("User not found or inactive")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Ensure the current user is active."""
    if not current_user.is_active:
        raise ForbiddenException("Account is deactivated")
    return current_user


class RoleRequired:
    """Dependency that checks if the current user has the required role."""

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        if current_user.role and current_user.role.name in self.allowed_roles:
            return current_user
        raise ForbiddenException(
            f"Role '{current_user.role.name if current_user.role else 'none'}' "
            f"is not authorized. Required: {', '.join(self.allowed_roles)}"
        )


# Pre-configured role dependencies
require_super_admin = RoleRequired(["super_admin"])
require_hr_admin = RoleRequired(["super_admin", "hr_admin"])
require_manager = RoleRequired(["super_admin", "hr_admin", "department_manager"])
require_employee = RoleRequired(["super_admin", "hr_admin", "department_manager", "employee"])
