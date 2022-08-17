"""Exceptions to raise on /users endpoints."""
from fastapi import status
from fastapi import HTTPException

USER_EXIST_CONFLICT = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists.",
)

USER_CREDENTIALS_UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unable to validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)

USER_INACTIVE_FORBIDDEN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is currently inactive.",
    headers={"WWW-Authenticate": "Bearer"},
)