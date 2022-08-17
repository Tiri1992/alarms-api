"""Authentication using oauth2."""
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from jose import JWTError
from jose import jwt
from typing import Any
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timedelta
from app.schemas.tokens import TokenData
from app.core.config import settings

# tokenUrl declares the path that client needs to use to get token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1}/auth/login")

class Token(ABC):

    @abstractmethod
    def create(self):
        pass 

    @abstractmethod
    def validate(self):
        pass

class JWT(Token):
    """Issue tokens and verifying their validity.

    Attributes:
        expires: Time in minutes when the token should expire.
        algorithm: Encryption algorithm. See python-jose documentation.
        secret_key: Used to sign the webtoken. Must be stored safely.
    """
    def __init__(self, expires: int, algorithm: str, secret_key: str) -> None:
        self._expires = expires 
        self._algorithm = algorithm
        self._secret_key = secret_key

    def create(self, data: dict[str, Any]):
        to_encode = data.copy()
        to_encode.update(
            {
                "exp": datetime.utcnow() + timedelta(minutes=self._expires)
            }
        )
        return jwt.encode(
            claims=to_encode,
            key=self._secret_key,
            algorithm=self._algorithm,
        )

    def validate(self, token: str, credentials_exception: HTTPException) -> TokenData:
        try:
            res = jwt.decode(
                token=token,
                key=self._secret_key,
                algorithms=self._algorithm,
            ) 
            email: str = res.get("email")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        return token_data 

    @classmethod
    def from_settings(cls):
        """Builds constructor from environment configs declared
        in app.core.config.settings.

        Returns:
            JWT: Instance with assigned attributes retrieved 
                from environment configs.
        """
        return cls(
            expires=settings.access_token_expire_minutes,
            algorithm=settings.algorithm,
            secret_key=settings.secret_key,
        )


jwt_api = JWT.from_settings()