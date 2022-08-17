"""Exceptions to raise on /login endpoint."""
from fastapi import status
from fastapi import HTTPException

INVALID_CREDENTIALS_UNATHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials. Either username or password is incorrect.",
    headers={"WWW-Authenticate": "Bearer"},
)