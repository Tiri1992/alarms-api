"""Response schemas for API."""
from pydantic import BaseModel
from pydantic import EmailStr
from datetime import datetime


# Base config

class UserBase(BaseModel):

    email: EmailStr


class UserCreate(UserBase):

    phone_number: str
    password: str


class UserLogin(UserBase):

    password: str


class User(UserBase):
    """Returned obj when user calls get_user."""
    id: int
    phone_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
