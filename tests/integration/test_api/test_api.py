import urllib.parse
from http import HTTPStatus

from api.flights_api.api_endpoints import (app, get_departure_flights,
                                           get_return_flights, ping)


def test_ping(client):
    url = app.url_path_for(ping.__name__)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == "pong"


def test_get_departure_flights(client):
    url = app.url_path_for(get_departure_flights.__name__)
    params = {
        "origin": "LHR",
        "departure_date": "2023-05-25",
        "destination": "ZRH",
    }
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    response = client.get(full_url)
    assert response.status_code == HTTPStatus.OK, response.json()
    flights = response.json()
    assert len(flights) == 29
    for flight in flights:
        assert not flight["date"].isnumeric()


def test_get_return_flights(client):
    url = app.url_path_for(get_return_flights.__name__)
    params = {
        "origin": "ZRH",
        "destination": "LHR",
        "return_date": "2023-06-01",
    }
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    response = client.get(full_url)
    assert response.status_code == HTTPStatus.OK, response.json()
    flights = response.json()
    assert len(flights) == 14
    for flight in flights:
        assert not flight["date"].isnumeric()
