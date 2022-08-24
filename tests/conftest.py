"""Resuable fixtures across entire test suite."""
import pytest 
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.api.deps import get_db
from app.database.db import Base
from app.main import app
from app.core.oauth2 import jwt_api
from app.core.config import settings


engine = create_engine(url=settings.postgres_uri_test)
# Drop then recreate
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="function")
def session():
    # Drop schema initially to test on clean db
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    # override the get_db() dependency injection to point to
    # test db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture(scope="function")
def test_user(client):
    user_data = {
        "email": "example@gmail.com",
        "phone_number": "07822341834",
        "password": "pass123"
    }
    # Create user -> returns UserDBSchema, so missing pw
    res = client.post(f"{settings.API_V1}/users/", json=user_data)

    # Verify it was created
    assert res.status_code == 201
    data = res.json()
    # Reassign pw to returned object so that it can
    # be used to create jwt
    data["password"] = user_data["password"]
    return data 


@pytest.fixture(scope="function")
def jwt_token(test_user):
    # Creates access_token

    access_token = jwt_api.create(
        data={
            "email": test_user["email"],
            "user_id": test_user["id"],
        }
    )
    return access_token

@pytest.fixture(scope="function")
def authorised_client(client, jwt_token):
    # We need to pass in as a header {"Authorization: "Bearer $access_token"}
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {jwt_token}"
    }

    return client