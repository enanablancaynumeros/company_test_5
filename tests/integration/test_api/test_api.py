from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from api.phone_api.alembic.utils import recreate_postgres_metadata
from api.phone_api.api_endpoints import app, get_phone_calls_history, ping

client = TestClient(app)


@pytest.fixture(autouse=True)
def db_recreate():
    recreate_postgres_metadata()


def test_ping():
    url = app.url_path_for(ping.__name__)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == "pong"


def test_get_calls():
    url = app.url_path_for(get_phone_calls_history.__name__, phone_id=1)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"msg": "Hello World"}
