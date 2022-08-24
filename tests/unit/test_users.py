"""Unittesting routers asssociated to the /users endpoint."""
from app.core.config import settings

def test_identify_user(authorised_client):
    res = authorised_client.get(f"{settings.API_V1}/users/caller")

    assert res.status_code == 200