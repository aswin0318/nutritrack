"""Admin API routes."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_hr_admin, require_super_admin
from app.models.audit import AuditLog
from app.models.user import User
from app.services.user import UserService
from app.services.organization import DepartmentService
from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.utils.pagination import PaginatedResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=PaginatedResponse)
async def admin_list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    current_user: User = Depends(require_hr_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all users (HR Admin+)."""
    service = UserService(db)
    skip = (page - 1) * page_size
    users, total = await service.get_organization_users(
        current_user.organization_id, skip=skip, limit=page_size, search=search
    )
    items = [
        {
            "id": str(u.id),
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "role": u.role.name if u.role else None,
            "department": u.department.name if u.department else None,
            "is_active": u.is_active,
            "wellness_score": u.wellness_score,
            "created_at": str(u.created_at),
        }
        for u in users
    ]
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)


@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: UUID,
    current_user: User = Depends(require_hr_admin),
    db: AsyncSession = Depends(get_db),
):
    """Deactivate a user (HR Admin+)."""
    service = UserService(db)
    await service.deactivate_user(user_id)
    return {"message": "User deactivated"}


@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: UUID,
    current_user: User = Depends(require_hr_admin),
    db: AsyncSession = Depends(get_db),
):
    """Activate a user (HR Admin+)."""
    service = UserService(db)
    await service.activate_user(user_id)
    return {"message": "User activated"}


@router.get("/departments", response_model=list[DepartmentResponse])
async def list_departments(
    current_user: User = Depends(require_hr_admin),
    db: AsyncSession = Depends(get_db),
):
    """List departments (HR Admin+)."""
    service = DepartmentService(db)
    depts = await service.list_by_org(current_user.organization_id)
    return [DepartmentResponse(
        id=d.id, name=d.name, code=d.code, description=d.description,
        is_active=d.is_active, organization_id=d.organization_id,
        manager_id=d.manager_id,
        manager_name=d.manager.full_name if d.manager else None,
        employee_count=len(d.users) if d.users else 0,
        created_at=d.created_at, updated_at=d.updated_at,
    ) for d in depts]


@router.post("/departments", response_model=DepartmentResponse, status_code=201)
async def create_department(
    data: DepartmentCreate,
    current_user: User = Depends(require_hr_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a department (HR Admin+)."""
    service = DepartmentService(db)
    dept = await service.create({
        **data.model_dump(),
        "organization_id": current_user.organization_id,
    })
    return DepartmentResponse(
        id=dept.id, name=dept.name, code=dept.code, description=dept.description,
        is_active=dept.is_active, organization_id=dept.organization_id,
        manager_id=dept.manager_id, employee_count=0,
        created_at=dept.created_at, updated_at=dept.updated_at,
    )


@router.get("/audit-logs", response_model=PaginatedResponse)
async def list_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    action: Optional[str] = None,
    current_user: User = Depends(require_super_admin),
    db: AsyncSession = Depends(get_db),
):
    """List audit logs (Super Admin only)."""
    from sqlalchemy import func, desc
    query = select(AuditLog).where(
        AuditLog.organization_id == current_user.organization_id
    )
    if action:
        query = query.where(AuditLog.action.ilike(f"%{action}%"))
    query = query.order_by(desc(AuditLog.created_at))

    # Count
    count_q = select(func.count(AuditLog.id)).where(
        AuditLog.organization_id == current_user.organization_id
    )
    total_result = await db.execute(count_q)
    total = total_result.scalar_one()

    skip = (page - 1) * page_size
    query = query.offset(skip).limit(page_size)
    result = await db.execute(query)
    logs = result.scalars().all()

    items = [
        {
            "id": str(log.id),
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "description": log.description,
            "ip_address": log.ip_address,
            "user_id": str(log.user_id) if log.user_id else None,
            "created_at": str(log.created_at),
        }
        for log in logs
    ]
    return PaginatedResponse.create(items=items, total=total, page=page, page_size=page_size)
