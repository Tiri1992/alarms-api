"""Collection of api routers to use in version 1."""
from fastapi import APIRouter

from app.api.api_v1.routers import general
from app.api.api_v1.routers import alarms

# init
router = APIRouter()

# Routes for V1
router.include_router(general.router)
router.include_router(alarms.router)
