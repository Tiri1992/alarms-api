"""Main script."""

from fastapi import FastAPI
# Api routers
from app.api.api_v1 import api as apiv1
from app.core.config import settings
# DB init
from app.database.db import Base, engine
# This will help load models to map
from app.models.alarms import Alarms

Base.metadata.create_all(engine)

app = FastAPI(
    title="Alarms API",
)

# Version 1, this will scale on version 2.
app.include_router(apiv1.router, prefix=settings.API_V1)
