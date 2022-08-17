"""Response models for returned data from server."""
import datetime
from pydantic import BaseModel, Field
from typing import Union


class AlarmBaseSchema(BaseModel):

    is_on: Union[bool, None]
    message: str = Field(...,
                         max_length=150, description="Message has a max char count of 150.")


class AlarmCreateSchema(AlarmBaseSchema):
    day_of_week: int = Field(..., ge=1, le=7,
                             description="Day of week, Monday=1, Sunday=7.")
    time: datetime.time

class AlarmDeleteSchema(AlarmBaseSchema):
    day_of_week: int = Field(..., ge=1, le=7,
                             description="Day of week, Monday=1, Sunday=7.")
    time: datetime.time 

class AlarmUpdateSchema(AlarmBaseSchema):
    day_of_week: int = Field(..., ge=1, le=7,
                             description="Day of week, Monday=1, Sunday=7.")
    time: datetime.time 
    updated_at: Union[datetime.datetime, None]


class AlarmDBSchema(AlarmBaseSchema):

    id: int
    day_of_week: int = Field(..., ge=1, le=7,
                             description="Day of week, Monday=1, Sunday=7.")
    time: datetime.time
    created_at: datetime.datetime
    updated_at: Union[datetime.datetime, None]

    class Config:
        orm_mode = True
