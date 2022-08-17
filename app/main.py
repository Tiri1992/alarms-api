"""Main script."""
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
# Api routers
from app.api.api_v1 import api as apiv1
from app.core.config import settings
# Securities
from app.core.oauth2 import oauth2_scheme

# Base.metadata.create_all(engine)

app = FastAPI(
    title="Alarms API",
)

# Version 1, this will scale on version 2.
app.include_router(apiv1.router, prefix=settings.API_V1)