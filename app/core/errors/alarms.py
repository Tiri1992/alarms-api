"""Exceptions to raise on /alarms endpoints."""
from fastapi import status
from fastapi import HTTPException

ALARM_EXISTS_CONFLICT = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Alarm currently exists for user. If alarm is inactive, then reactivate.",
)

ALARM_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Alarm does not exist.",
)
