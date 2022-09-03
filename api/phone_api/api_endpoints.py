from fastapi import FastAPI, Response, status

from .db_connection import recreate_postgres_metadata
from .handlers import CallsHandler
from .schemas import CallSchema

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    recreate_postgres_metadata()


@app.get(path="/ping")
async def ping():
    return "pong"


@app.post(path="/call", status_code=status.HTTP_201_CREATED)
async def post_customer_call(call: CallSchema):
    return CallsHandler.save_user_call(call=call)


@app.get(path="/phone/{phone_id}/history")
async def get_phone_calls_history(phone_id: int):
    return CallsHandler.get_user_calls(phone_id=phone_id)
