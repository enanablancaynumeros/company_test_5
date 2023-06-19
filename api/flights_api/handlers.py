from concurrent.futures import ThreadPoolExecutor

import pendulum

from .api_requests import ApiRequest


class DataCollector:
    @classmethod
    def get_departure_trips(
        cls, origin: str, destination: str, departure_date: str
    ) -> list[dict]:
        return cls.execute(date=departure_date, origin=origin, destination=destination)

    @classmethod
    def get_return_trips(
        cls, origin: str, destination: str, return_date: str
    ) -> list[dict]:
        return cls.execute(date=return_date, origin=origin, destination=destination)

    @classmethod
    def execute(cls, date: str, origin: str, destination: str) -> list[dict]:
        futures = []
        with ThreadPoolExecutor(max_workers=3) as executor_returns:
            futures.append(
                executor_returns.submit(
                    ApiRequest.get_quick_wings,
                    date=date,
                    origin=origin,
                    destination=destination,
                )
            )
            futures.append(
                executor_returns.submit(
                    ApiRequest.get_my_wings,
                    date=date,
                    origin=origin,
                    destination=destination,
                )
            )
            futures.append(
                executor_returns.submit(
                    ApiRequest.get_cheap_air,
                    date=date,
                    origin=origin,
                    destination=destination,
                )
            )

        results = []
        for future in futures:
            result = future.result()
            results.extend(result)

        converted_flights = ConvertFlights.convert_to_date_objects(results)
        sorted_flights = list(sorted(converted_flights, key=lambda x: x["date"]))
        return ConvertFlights.serialize_dates(sorted_flights)


class ConvertFlights:
    @staticmethod
    def convert_to_date_objects(flights: list[dict]) -> list[dict]:
        converted_flights = []
        for flight in flights:
            # cheap air case
            if "date" not in flight:
                converted_date = pendulum.parse(flight["departure_date"])
            elif isinstance(flight["date"], str):
                converted_date = pendulum.parse(flight["date"])
            else:
                # unix timestamp
                converted_date = pendulum.from_timestamp(flight["date"])

            converted_flight = {**flight, "date": converted_date}
            converted_flights.append(converted_flight)
        return converted_flights

    @staticmethod
    def serialize_dates(flights: list[dict]):
        for flight in flights:
            flight["date"] = flight["date"].to_iso8601_string()
        return flights
