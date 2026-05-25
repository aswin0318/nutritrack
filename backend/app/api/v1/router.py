"""API v1 router aggregation."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.challenges import router as challenges_router
from app.api.v1.events import router as events_router
from app.api.v1.rewards import router as rewards_router
from app.api.v1.activities import router as activities_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.admin import router as admin_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(challenges_router)
api_router.include_router(events_router)
api_router.include_router(rewards_router)
api_router.include_router(activities_router)
api_router.include_router(analytics_router)
api_router.include_router(admin_router)
