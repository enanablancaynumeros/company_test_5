import pytest
from fastapi.testclient import TestClient

from api.flights_api.api_endpoints import app


@pytest.fixture()
def client():
    return TestClient(app)
