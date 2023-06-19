import datetime

from pydantic import BaseModel


class FlightSchema(BaseModel):
    origin: str
    destination: str
    date: int | str
    flight_duration: int
    currency: str
    price: int


class FlightsSchema(BaseModel):
    departure_flights: list[FlightSchema]
    return_flights: list[FlightSchema]
