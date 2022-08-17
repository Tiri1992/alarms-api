"""models for representing issued tokens."""
from pydantic import BaseModel
from pydantic import EmailStr

class Token(BaseModel):

    access_token: str 
    token_type: str

class TokenData(BaseModel):

    email: EmailStr