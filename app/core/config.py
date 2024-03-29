"""Configurations for api endpoints."""

from enum import Enum, unique
from pydantic import BaseSettings
from pydantic import PostgresDsn
from functools import lru_cache


@unique
class Tags(str, Enum):

    GENERAL = "General"
    AUTH = "Auth"
    ALARMS = "Alarms"
    USERS = "Users"

class Settings(BaseSettings):

    API_V1: str = "/api/v1"

    root_user: str
    root_password: str
    postgres_uri: PostgresDsn
    postgres_uri_test: PostgresDsn
    secret_key: str 
    algorithm: str 
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Cache environment variables so they are not reloaded with each request

@lru_cache
def load_settings() -> Settings:
    return Settings()


settings = load_settings()
