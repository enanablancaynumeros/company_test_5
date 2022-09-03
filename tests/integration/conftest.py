import datetime

import pytest
from fastapi.testclient import TestClient
from phone_api.db_connection import recreate_postgres_metadata

from api.phone_api.api_endpoints import app

CUSTOMER_PHONE = "0000"
FREEZE_DATE = "2020-04-08"


@pytest.fixture(autouse=True)
def db_recreate():
    recreate_postgres_metadata()


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def customer_with_phone():
    from phone_api.handlers import CustomerHandler

    new_customer = CustomerHandler.add(
        name="Yeray", email="yeray.alvarez.romero@gmail.com"
    )
    return CustomerHandler.add_phone(
        customer_id=new_customer["id"], phone_number=CUSTOMER_PHONE
    )


@pytest.mark.freeze_time(FREEZE_DATE)
@pytest.fixture()
def calls():
    from phone_api.handlers import CallsHandler
    from phone_api.schemas import CallSchema

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
