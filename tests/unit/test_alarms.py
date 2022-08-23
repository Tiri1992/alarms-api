"""Unittests associated to /alarms endpoints."""
from app.core.config import settings

def test_get_alarms(authorised_client):
    """Validates GET HTTP method to the path operation alarms/"""
    res = authorised_client.get(f"{settings.API_V1}/alarms/")

    assert res.status_code == 200

    data = res.json()
    # should return a list type
    assert isinstance(data, list)
    # No records should be populated as we dont pass `alarm_init`
    # into signature of test func
    assert len(data) == 0

def test_create_alarms(authorised_client):
    """Validates POST HTTP method on the path operation alarms/""" 

    body = {
        "is_on": True, 
        "message": "test message.",
        "day_of_week": 2,
        "time": "17:00:00",
    }
    # ending in /
    res = authorised_client.post(f"{settings.API_V1}/alarms/", json=body)

    res_create = res.json()

    assert res.status_code == 201
    
    # object validatation (except created_at time)
    assert res_create["is_on"] == True 
    assert res_create["message"] == "test message."
    assert res_create["day_of_week"] == 2
    assert res_create["time"] == "17:00:00+00:00"

def test_delete_alarms(authorised_client, alarm_init):
    
    alarm_id = alarm_init["id"]

    res_delete = authorised_client.delete(f"{settings.API_V1}/alarms/{alarm_id}")

    assert res_delete.status_code == 204



def test_update_alarms(authorised_client, alarm_init):
    
    body_to_update = {
        "is_on": alarm_init["is_on"],
        "message": alarm_init["message"],
        "day_of_week": alarm_init["day_of_week"],
        "time": "18:00:00",
    }
    alarm_id = alarm_init["id"]

    res_update = authorised_client.put(f"{settings.API_V1}/alarms/{alarm_id}", json=body_to_update)

    data_update = res_update.json()

    assert res_update.status_code == 200

    # check time was updated
    assert data_update["time"] == "18:00:00+00:00"
    