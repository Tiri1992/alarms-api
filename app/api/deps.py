"""Dependencies for our api_v1."""
from typing import Generator
from app.database.db import SessionLocal


def get_db() -> Generator:
    # establish Session to db then cleans up resources
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
