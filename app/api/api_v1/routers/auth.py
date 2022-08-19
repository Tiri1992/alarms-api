"""Authentication for users using JWT token."""
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status 
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.tokens import Token
from app.core.oauth2 import jwt_api
from app.core.security import user_hash
from app.core.controller.users import CrudUser
from app.core.controller.auth import CheckAuth
from app.core.config import Tags

router = APIRouter(
    prefix="/auth",
    tags=[Tags.AUTH],
)

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # Instantiate CrudUser obj
    crud = CrudUser(db=db)
    # Get user record from db. username in passed in by client Form will be email
    user = crud.get(email=user_credentials.username)
    check = CheckAuth(user=user)
    # Validate user exists
    check.exists()
    # Validate user password
    check.correct_password(
        password=user_credentials.password,
        user_hash=user_hash,
    )
    # Create access token
    access_token = jwt_api.create(
        data={
            "email": user.email,
            "user_id": user.id,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }