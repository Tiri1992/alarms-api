"""Endpoints for user resources."""
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.config import Tags
# Schemas
from app.schemas import users as schemas
# Models
from app.models import users as models
# Controller
from app.core.controller.users import CrudUser
from app.core.controller.users import get_current_active_user
from app.core.controller.users import CheckUser
# Security
from app.core.security import user_hash


router = APIRouter(
    prefix="/users",
    tags=[Tags.USERS],
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserDBSchema)
def create_user(user: schemas.UserCreateSchema, db: Session = Depends(get_db)):
    # Fail if user already exists
    check = CheckUser(db)
    check.exists(email=user.email)
    # Create user
    crud = CrudUser(db)
    # Inplace change to hash pw in user request body
    user_persist = user_hash.hash_password(user)
    # Create user
    response = crud.create(user_persist)
    return response

@router.get("/caller", status_code=status.HTTP_200_OK ,response_model=schemas.UserDBSchema)
def identify_user(user: models.UserModel = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return user