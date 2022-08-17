"""Utility functions associated to hashing and securing client data."""
from passlib.context import CryptContext
from abc import ABC, abstractmethod
from app.schemas.users import UserCreateSchema

class Security(ABC):

    @abstractmethod
    def apply(self):
        pass 

    @abstractmethod
    def validate(self):
        pass


class Hash(Security):

    def __init__(self, hash_algo: str) -> None:
        self._context = CryptContext(schemes=[hash_algo], deprecated="auto")

    def apply(self, password: str) -> str:
        return self._context.hash(password)
    
    def validate(self, password: str, password_hashed: str) -> bool:
        return self._context.verify(password,password_hashed)


class UserHash(Hash):

    def __init__(self, hash_algo: str) -> None:
        super().__init__(hash_algo)

    def hash_password(self, schema: UserCreateSchema) -> UserCreateSchema:
        """hash_password will get password from 
        data model and hash it using algorithm defined.

        Args:
            schema (UserCreateSchema): client object parsed
                as a pydantic model when creating a user.

        Returns:
            UserCreateSchema: client object after password is
                hashed.
        """
        schema.password = super().apply(schema.password)
        return schema

user_hash = UserHash(hash_algo="bcrypt")