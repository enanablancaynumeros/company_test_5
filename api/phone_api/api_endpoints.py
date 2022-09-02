from fastapi import FastAPI

from .handler import CallsHandler
from .schemas import Call

app = FastAPI()


@app.get(path="/ping")
async def ping():
    return "pong"


@app.post(path="/call")
async def post_customer_call(call: Call):
    res = CallsHandler.save_user_call(call=call)
    return {"message": "Hello World"}


@app.get(path="/phone/{phone_id}/history")
async def get_phone_calls_history(phone_id: int):
    return CallsHandler.get_user_calls(phone_id=phone_id)
