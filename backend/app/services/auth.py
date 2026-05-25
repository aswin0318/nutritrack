"""Authentication service."""

from datetime import timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.config import get_settings
from app.exceptions import BadRequestException, ConflictException, NotFoundException, UnauthorizedException
from app.models.user import Role, User
from app.repositories.user import UserRepository
from app.repositories.organization import OrganizationRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    create_password_reset_token,
    decode_token,
    hash_password,
    verify_password,
)

logger = structlog.get_logger()
settings = get_settings()


class AuthService:
    """Service handling authentication operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.org_repo = OrganizationRepository(db)

    async def login(self, request: LoginRequest) -> TokenResponse:
        """Authenticate user and return tokens."""
        user = await self.user_repo.get_by_email(request.email)

        if not user or not verify_password(request.password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedException("Account is deactivated")

        role_name = user.role.name if user.role else "employee"

        access_token = create_access_token(
            subject=str(user.id),
            role=role_name,
            organization_id=str(user.organization_id),
        )
        refresh_token = create_refresh_token(subject=str(user.id))

        logger.info("user_login", user_id=str(user.id), email=user.email)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.jwt_access_token_expire_minutes * 60,
        )

    async def register(self, request: RegisterRequest) -> TokenResponse:
        """Register a new user."""
        existing = await self.user_repo.get_by_email(request.email)
        if existing:
            raise ConflictException("Email already registered")

        # Get or create default organization
        from sqlalchemy import select
        org = None
        if request.organization_name:
            org = await self.org_repo.create({
                "name": request.organization_name,
            })
        else:
            result = await self.db.execute(
                select(self.org_repo.model).limit(1)
            )
            org = result.scalar_one_or_none()
            if not org:
                org = await self.org_repo.create({"name": "Default Organization"})

        # Get default employee role
        from sqlalchemy import select as sel
        result = await self.db.execute(sel(Role).where(Role.name == "employee"))
        role = result.scalar_one_or_none()
        if not role:
            role = Role(name="employee", display_name="Employee", is_system=True)
            self.db.add(role)
            await self.db.flush()

        user = await self.user_repo.create({
            "email": request.email,
            "password_hash": hash_password(request.password),
            "first_name": request.first_name,
            "last_name": request.last_name,
            "employee_id": request.employee_id,
            "organization_id": org.id,
            "role_id": role.id,
        })

        access_token = create_access_token(
            subject=str(user.id),
            role=role.name,
            organization_id=str(org.id),
        )
        refresh_token = create_refresh_token(subject=str(user.id))

        logger.info("user_registered", user_id=str(user.id), email=user.email)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.jwt_access_token_expire_minutes * 60,
        )

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Refresh an access token."""
        try:
            payload = decode_token(refresh_token)
        except ValueError:
            raise UnauthorizedException("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid token type")

        user_id = payload.get("sub")
        user = await self.user_repo.get_by_id_with_relations(UUID(user_id))

        if not user or not user.is_active:
            raise UnauthorizedException("User not found or inactive")

        role_name = user.role.name if user.role else "employee"

        new_access_token = create_access_token(
            subject=str(user.id),
            role=role_name,
            organization_id=str(user.organization_id),
        )
        new_refresh_token = create_refresh_token(subject=str(user.id))

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.jwt_access_token_expire_minutes * 60,
        )

    async def forgot_password(self, email: str) -> dict:
        """Generate a password reset token."""
        user = await self.user_repo.get_by_email(email)
        if not user:
            # Don't reveal whether email exists
            return {"message": "If an account exists with this email, a reset link has been sent."}

        token = create_password_reset_token(email)
        logger.info("password_reset_requested", email=email)

        # In production, send email. For now, return token.
        return {
            "message": "If an account exists with this email, a reset link has been sent.",
            "reset_token": token,  # Remove in production; send via email instead
        }

    async def reset_password(self, token: str, new_password: str) -> dict:
        """Reset password using a reset token."""
        try:
            payload = decode_token(token)
        except ValueError:
            raise BadRequestException("Invalid or expired reset token")

        if payload.get("type") != "password_reset":
            raise BadRequestException("Invalid token type")

        email = payload.get("sub")
        user = await self.user_repo.get_by_email(email)

        if not user:
            raise NotFoundException("User")

        await self.user_repo.update(user.id, {
            "password_hash": hash_password(new_password),
        })

        logger.info("password_reset_completed", user_id=str(user.id))
        return {"message": "Password has been reset successfully"}
