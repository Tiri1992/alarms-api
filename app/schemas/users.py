"""Response schemas for API."""
from pydantic import BaseModel
from pydantic import EmailStr
from datetime import datetime
from typing import Union

# Base config

class UserBaseSchema(BaseModel):

    email: EmailStr


class UserCreateSchema(UserBaseSchema):

    phone_number: str
    password: str


class UserLoginSchema(UserBaseSchema):

    password: str

class UserUpdateSchema(UserBaseSchema):
    # Although it overlaps with UserLoginSchema
    # For consistancy I've kept these separate
    phone_number: str


class UserDBSchema(UserBaseSchema):
    """Returned obj when user calls get_user."""
    id: int
    phone_number: str
    is_active: bool
    created_at: datetime
    updated_at: Union[datetime, None]

    class Config:
        orm_mode = True