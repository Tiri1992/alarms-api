"""These endpoints are for general testing."""
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from app.core.config import Tags
# Security
from app.core.oauth2 import oauth2_scheme
# Schemas
from app.schemas.users import UserFake, UserFakeInDB

router = APIRouter(
    prefix="/general",
    tags=[Tags.GENERAL]
)


@router.get("/")
def get_hello(token: str = Depends(oauth2_scheme)):
    return {
        "message": "Hello, World!",
        "token": token
    }
