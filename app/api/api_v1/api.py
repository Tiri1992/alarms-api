"""Collection of api routers to use in version 1."""
from fastapi import APIRouter

from app.api.api_v1.routers import alarms
from app.api.api_v1.routers import users
from app.api.api_v1.routers import auth
# init
router = APIRouter()

# Routes for V1
router.include_router(alarms.router)
router.include_router(users.router)
router.include_router(auth.router)