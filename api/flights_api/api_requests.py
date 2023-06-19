import urllib.parse

import requests
from flights_api.exceptions import ApiError, InvalidRequest
from flights_api.schemas import FlightSchema
from tenacity import retry, retry_if_exception_type, stop_after_attempt


class ApiRequest:
    @classmethod
    def get_quick_wings(
        cls, date: str, origin: str, destination: str
    ) -> list[FlightSchema]:
        base_url = "https://flight-api-exercise.vercel.app/api/quick-wings"
        params = {
            "departure_date": date,
            "origin": origin,
            "destination": destination,
        }
        return cls.make_request(base_url=base_url, params=params)

    @classmethod
    def get_my_wings(
        cls, date: str, origin: str, destination: str
    ) -> list[FlightSchema]:
        base_url = "https://flight-api-exercise.vercel.app/api/mywings"
        params = {
            "date": date,
            "origin": origin,
            "destination": destination,
        }
        return cls.make_request(base_url=base_url, params=params)

    @classmethod
    def get_cheap_air(
        cls, date: str, origin: str, destination: str
    ) -> list[FlightSchema]:
        base_url = "https://flight-api-exercise.vercel.app/api/cheapair"
        params = {
            "from_date": date,
            "from_code": origin,
            "to_code": destination,
        }
        return cls.make_request(base_url=base_url, params=params)

    @classmethod
    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(ApiError))
    def make_request(cls, base_url, params):
        full_url = f"{base_url}?{urllib.parse.urlencode(params)}"
        response = requests.get(full_url)
        if response.status_code >= 500:
            raise ApiError()
        if response.status_code == 400:
            raise InvalidRequest()
        return response.json()
