"""These endpoints are for general testing."""
from fastapi import APIRouter
from app.core.config import Tags

router = APIRouter(
    prefix="/general",
    tags=[Tags.GENERAL]
)


@router.get("/")
def get_hello():
    return {
        "message": "Hello, World!"
    }
