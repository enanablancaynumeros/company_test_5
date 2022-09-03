import datetime
import json
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from starlette import status

from api.phone_api.alembic.utils import recreate_postgres_metadata
from api.phone_api.api_endpoints import (app, get_phone_calls_history, ping,
                                         post_customer_call)
from api.phone_api.handlers import CallsHandler, CustomerHandler
from api.phone_api.schemas import CallSchema

client = TestClient(app)

CUSTOMER_PHONE = "0000"
FREEZE_DATE = "2020-04-08"


@pytest.fixture(autouse=True)
def db_recreate():
    recreate_postgres_metadata()


def test_ping():
    url = app.url_path_for(ping.__name__)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == "pong"


@pytest.fixture()
def customer_with_phone():
    new_customer = CustomerHandler.add(
        name="Yeray", email="yeray.alvarez.romero@gmail.com"
    )
    return CustomerHandler.add_phone(
        customer_id=new_customer["id"], phone_number=CUSTOMER_PHONE
    )


@pytest.mark.freeze_time(FREEZE_DATE)
@pytest.fixture()
def calls():
    call_1 = CallsHandler.save_user_call(
        call=CallSchema(
            source_phone=CUSTOMER_PHONE,
            target_phone_number="0001",
            duration_in_minutes=1,
            start_time=datetime.datetime.today(),
        )
    )
    call_2 = CallsHandler.save_user_call(
        call=CallSchema(
            source_phone=CUSTOMER_PHONE,
            target_phone_number="0002",
            duration_in_minutes=10,
            start_time=datetime.datetime.today(),
        )
    )
    return call_1, call_2


@pytest.mark.freeze_time(FREEZE_DATE)
def test_get_calls(customer_with_phone, calls):
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


def test_get_calls_non_existing_customer():
    url = app.url_path_for(get_phone_calls_history.__name__, phone_id=0)
    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Phone 0 not found"}


@pytest.mark.freeze_time(FREEZE_DATE)
def test_post_user_call(customer_with_phone):
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
