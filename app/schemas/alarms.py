"""Response models for returned data from server."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union


class AlarmBase(BaseModel):

    is_on: Union[bool, None]
    message: str = Field(...,
                         max_length=160, description="Message has a max char count of 160.")


class AlarmCreate(AlarmBase):
    day_of_week: int = Field(..., ge=1, le=7,
                             description="Day of week, Monday=1, Sunday=7.")
    hour: int = Field(..., ge=1, le=24,
                      description="Hour within 24 hour clock.")


class AlarmUpdate(AlarmBase):
    updated_at: Union[datetime, None]


class Alarm(AlarmBase):

    id: int
    day_of_week: int = Field(..., ge=1, le=7,
                             description="Day of week, Monday=1, Sunday=7.")
    hour: int = Field(..., ge=1, le=24,
                      description="Hour within 24 hour clock.")
    created_at: datetime
    updated_at: Union[datetime, None]

    class Config:
        orm_mode = True
