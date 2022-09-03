import datetime
import json
from http import HTTPStatus

import pytest
from starlette import status

from api.phone_api.api_endpoints import (app, get_phone_calls_history,
                                         get_phone_invoice, ping,
                                         post_customer_call)
from api.phone_api.schemas import CallSchema
from tests.integration.conftest import CUSTOMER_PHONE, FREEZE_DATE


def test_ping(client):
    url = app.url_path_for(ping.__name__)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == "pong"


@pytest.mark.freeze_time(FREEZE_DATE)
def test_get_calls(client, customer_with_phone, calls):
    url = app.url_path_for(
        get_phone_calls_history.__name__, phone_id=customer_with_phone["id"]
    )
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    calls = response.json()
    for call in calls:
        assert call.pop("created")
        assert call.pop("id")

    assert calls == [
        {
            "duration_in_minutes": 1,
            "target_number": "0001",
            "start_time": f"{FREEZE_DATE}T00:00:00",
            "updated": None,
            "phone_id": customer_with_phone["id"],
        },
        {
            "duration_in_minutes": 10,
            "target_number": "0002",
            "start_time": f"{FREEZE_DATE}T00:00:00",
            "updated": None,
            "phone_id": customer_with_phone["id"],
        },
    ]


def test_get_calls_non_existing_customer(client):
    url = app.url_path_for(get_phone_calls_history.__name__, phone_id=0)
    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Phone 0 not found"}


@pytest.mark.freeze_time(FREEZE_DATE)
def test_post_user_call(client, customer_with_phone):
    url = app.url_path_for(post_customer_call.__name__)
    response = client.post(
        url=url,
        json=json.loads(
            CallSchema(
                source_phone=CUSTOMER_PHONE,
                target_phone_number="random",
                duration_in_minutes=3,
                start_time=datetime.datetime.today(),
            ).json()
        ),
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(
        app.url_path_for(
            get_phone_calls_history.__name__, phone_id=customer_with_phone["id"]
        )
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1
    assert response.json()[0]["duration_in_minutes"] == 3
    assert response.json()[0]["target_number"] == "random"


@pytest.mark.freeze_time(FREEZE_DATE)
def test_get_invoice(client, customer_with_phone, calls):
    url = app.url_path_for(
        get_phone_invoice.__name__, phone_id=customer_with_phone["id"]
    )
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["total_cost"] == 0.22
    assert response.json()["total_minutes"] == 11
    calls = response.json()["calls"]
    for call in calls:
        assert call.pop("created")
        assert call.pop("id")
    import ipdb

    ipdb.set_trace()
    assert calls == [
        {
            "duration_in_minutes": 1,
            "target_number": "0001",
            "start_time": f"{FREEZE_DATE}T00:00:00",
            "updated": None,
            "phone_id": customer_with_phone["id"],
        },
        {
            "duration_in_minutes": 10,
            "target_number": "0002",
            "start_time": f"{FREEZE_DATE}T00:00:00",
            "updated": None,
            "phone_id": customer_with_phone["id"],
        },
    ]
