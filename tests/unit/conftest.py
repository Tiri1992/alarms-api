"""Conftest for fixtures specific to unittests. 

In order to avoid making multiple post requests for creating client alarms for
testing DELETE and PUT http requests, we create a fixture that will post an alarm
to be used during startup.
"""
import pytest
from app.core.config import settings

@pytest.fixture(scope="function")
def alarm_init(authorised_client):
    """Fixture initialised user with a test alarm record."""
    body = {
        "is_on": True, 
        "message": "test message.",
        "day_of_week": 2,
        "time": "17:00:00",
    }
    
    res = authorised_client.post(f"{settings.API_V1}/alarms/", json=body)
    
    assert res.status_code == 201

    return res.json()
