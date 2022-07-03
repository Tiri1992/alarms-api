"""Module is responsible for creating an connection pool
and providing a session via an open connection."""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings
from pydantic import BaseSettings

engine = create_engine(
    url=settings.postgres_uri,
    echo=True
)


def establish_session(engine: Engine) -> sessionmaker:
    """Executing this function established session"""

    return sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )


# Init a local session to be used by path operations
SessionLocal = establish_session(engine)

# declarative base

Base = declarative_base()
