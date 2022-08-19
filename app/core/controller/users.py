"""Controller for users"""
from app.core.controller.base import CrudController
from app.core.controller.base import CheckController
from sqlalchemy.orm import Session
from fastapi import Depends
# Schemas
from app.schemas.users import UserCreateSchema
from app.schemas.users import UserUpdateSchema
from app.schemas.tokens import TokenData
# Models
from app.models.users import UserModel
# Oauth2
from app.core.oauth2 import jwt_api
from app.core.oauth2 import oauth2_scheme
# Exceptions
from app.core.errors.users import USER_EXIST_CONFLICT
from app.core.errors.users import USER_CREDENTIALS_UNAUTHORIZED
from app.core.errors.users import USER_INACTIVE_FORBIDDEN
# Utils
from app.api.deps import get_db
from datetime import datetime

class CrudUser(CrudController):

    def __init__(self, db: Session) -> None:
        self._db = db 
        self._model = UserModel

    def get(self, email: str) -> UserModel:
        """Get user model by email."""
        return self._db.query(self._model).filter(self._model.email == email).first()

    def create(self, schema: UserCreateSchema) -> UserModel:
        print(f"{schema=}")
        record = self._model(**schema.dict()) 
        # User is initialised as active
        record.is_active = True
        print(f"to insert -> {record.updated_at}")
        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record
        

    def delete(self, _id: int) -> None:
        """Delete user by user_id."""
        record = self._db.query(self._model).filter(self._model.id == _id)
        record.delete(synchronize_session=False)
        self._db.commit()

    def update(self, schema: UserUpdateSchema, _id: int) -> UserModel:
        record = self._db.query(self._model).filter(self._model.id == _id)
        schema.updated_at = datetime.now()
        record.update(schema.dict(), synchronize_session=False)
        self._db.commit()
        return record.first()

class CheckUser(CheckController):
    """Handler for validating any duplications of users
    before offsetting these requests to the database.
    """

    def __init__(self, db: Session) -> None:
        self._db = db 
        self._model = UserModel

    def exists(self, email: str) -> None:
        """Checks if user already exists in db and raises
        the user_exception if it does."""
        res = self._db.query(self._model).filter(self._model.email == email).first()
        if res:
            raise USER_EXIST_CONFLICT

# Get user helper functions
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
    """Retrieves user info based on the clients token.

    Args:
        token (str, optional): JWT token recieved from client.
        db (Session, optional): SQLAlchemy session object.

    Raises:
        credentials_exception: HTTP 401, server cannot verify token.

    Returns:
        UserModel: Record of user.
    """
    token_data: TokenData = jwt_api.validate(
        token=token,
        credentials_exception=USER_CREDENTIALS_UNAUTHORIZED,
    )
    crud = CrudUser(db=db)
    # Make a call to the server to retrieve user based on email
    user: UserModel = crud.get(email=token_data.email)
    # validate user exists
    if user is None:
        raise USER_CREDENTIALS_UNAUTHORIZED
    
    return user
     

async def get_current_active_user(user: UserModel = Depends(get_current_user)) -> UserModel:
    """Verifies if the current user is activated."""
    if not user.is_active:
        # Either 401 or 403 relevant. Leaning on latter due to account existing
        # except not valid
        raise USER_INACTIVE_FORBIDDEN
    return user