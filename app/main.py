"""Main script."""

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
# Api routers
from app.api.api_v1 import api as apiv1
from app.core.config import settings
# DB init
from app.database.db import Base, engine
# This will help load models to map
from app.models.alarms import Alarms
# Pydantic models
from app.schemas.users import UserFake, UserFakeInDB
# Securities
from app.core.oauth2 import oauth2_scheme

# Base.metadata.create_all(engine)

app = FastAPI(
    title="Alarms API",
)

# Version 1, this will scale on version 2.
app.include_router(apiv1.router, prefix=settings.API_V1)

# THIS IS AN EXAMPLE


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "fullname": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "somehashedpw",
        "disabled": False
    },
    "mary": {
        "username": "mary",
        "fullname": "Mary Green",
        "email": "mary@example.com",
        "hashed_password": "somehashedpw2",
        "disabled": True,
    }
}


def fake_hash_password(password: str):
    return "somehashed" + password


def get_user(db, username: str):
    if username in db:
        # This model inc. password attribute
        return UserFakeInDB(**db[username])

# Fake decoding token


def fake_decode_token(token):
    return get_user(fake_users_db, token)


def get_current_user(token: str = Depends(oauth2_scheme)):
    # User schema - pydantic model
    user = fake_decode_token(token)

    # If user doesnt exist, user variable will be none
    # this is the authentication stage
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWWW-Authenticate": "Bearer"}
        )
    return user


def get_current_active_user(current_user: UserFake = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user.")
    return current_user


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Look in db to get the user info
    user_dict = fake_users_db[form_data.username]
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect username or password.")
    # Instantiate the pydantic model from the user info retrieved from db
    user_valid = UserFakeInDB(**user_dict)
    # validate if the hashed pw is correct by checking the password hashed
    # against the password they sent in (hashed)
    if user_valid.hashed_password != fake_hash_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect username or password.")

    # Required to be complient with Oauth2
    # Response object of the /token endpoint should be json.
    # Needs token_type (bearer)
    return {
        "access_token": user_valid.username,
        "token_type": "bearer",
    }


@app.get("/users/me")
def read_users_me(current_user: UserFake = Depends(get_current_active_user)):
    # Dependency inject of get_current_active_user will run that function and
    # if user is not active will raise 400 http error
    return current_user
