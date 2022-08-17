"""Controller for auth"""
from fastapi import HTTPException
from fastapi import status
from app.core.controller.base import CheckController
from typing import Union
from app.models.users import UserModel
from app.core.security import Security
from app.core.errors.auth import INVALID_CREDENTIALS_UNATHORIZED

class CheckAuth(CheckController):

    def __init__(self, user: Union[UserModel, None] = None) -> None:
        self._user = user 

    def exists(self) -> None:
        """Check that the user attempting to authenticate actually exists. 
        If not raise credentials exception."""
        if not self._user:
            raise INVALID_CREDENTIALS_UNATHORIZED
    
    def correct_password(self, password: str, user_hash: Security) -> None:
        """Checks that client password matches the expected hashed password 
        stored for this user in the database. If not raise credentials exception."""
        pw_valid: bool = user_hash.validate(
            password=password,
            password_hashed=self._user.password,
        )
        if not pw_valid:
            raise INVALID_CREDENTIALS_UNATHORIZED
