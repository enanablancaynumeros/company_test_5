from fastapi import FastAPI

from .handlers import DataCollector
from .schemas import FlightSchema, FlightsSchema

app = FastAPI()

#
# @app.on_event("startup")
# async def startup_event():
#     # In a real world application we would orchestrate this differently before the API deployment,
#     # but this is sufficient for the exercise
#     recreate_postgres_metadata()


@app.get(path="/ping")
async def ping():
    return "pong"


@app.get(path="/departure_flights")
async def get_departure_flights(
    origin: str, destination: str, departure_date: str
) -> list[FlightSchema]:

    departure_flights = DataCollector.get_departure_trips(
        origin=origin, destination=destination, departure_date=departure_date
    )
    return departure_flights


@app.get(path="/return_flights")
async def get_return_flights(
    origin: str, destination: str, return_date: str
) -> list[FlightSchema]:
    return_flights = DataCollector.get_return_trips(
        origin=origin, destination=destination, return_date=return_date
    )
    return return_flights
