"""Integration test will test multiple endpoints from the /alarms 
URI http methods.
"""
from app.core.config import settings

def test_all_endpoints(authorised_client):
    """ 
    GIVEN authorised client
    WHEN client hits post, get, update, delete endpoints 
    for /alarms
    THEN check correct HTTP status is returned.
    """
    test_data = {
        "is_on": True, 
        "message": "Some cool message for integration test.",
        "day_of_week": 4,
        "time": "13:00:00",
    }
    response_post = authorised_client.post(f"{settings.API_V1}/alarms/", json=test_data)
    json_post = response_post.json()

    assert response_post.status_code == 201

    response_get = authorised_client.get(f"{settings.API_V1}/alarms/")

    json_get = response_get.json()

    assert response_get.status_code == 200

    # Should be one alarm created for current user
    assert len(json_get) == 1

    # Update: Turn off alarm
    test_data_update = json_post.copy()
    test_data_update["is_on"] = False 
    alarm_id = test_data_update["id"]

    response_update = authorised_client.put(f"{settings.API_V1}/alarms/{alarm_id}", json=test_data_update)

    json_update = response_update.json()

    assert response_update.status_code == 200
    # check update was made correctly
    assert json_update["is_on"] == False 

    # Delete
    response_delete = authorised_client.delete(f"{settings.API_V1}/alarms/{alarm_id}")

    assert response_delete.status_code == 204

    # Check that no alarms a present for current user

    response_get_after_delete = authorised_client.get(f"{settings.API_V1}/alarms/")

    response_get_after_delete_json = response_get_after_delete.json() 

    assert response_get_after_delete.status_code == 200

    # No alarms
    assert len(response_get_after_delete_json) == 0