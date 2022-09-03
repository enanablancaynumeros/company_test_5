from fastapi import HTTPException

from .data_models import CallsDBModel, CustomerDBModel, PhoneDBModel
from .db_connection import session_scope
from .schemas import CallSchema


class CallsHandler:
    @classmethod
    def save_user_call(cls, call: CallSchema) -> int:
        with session_scope() as session:
            existing_phone = (
                session.query(PhoneDBModel).filter_by(number=call.source_phone).one()
            )
            new_call = CallsDBModel(
                phone_id=existing_phone.id,
                start_time=call.start_time,
                target_number=call.target_phone_number,
                duration_in_minutes=call.duration_in_minutes,
            )
            session.add(new_call)
            return existing_phone.id

    @classmethod
    def get_user_calls(cls, phone_id: int):
        with session_scope() as session:
            if not session.query(session.query(PhoneDBModel).exists()).scalar():
                raise HTTPException(
                    status_code=404, detail=f"Phone {phone_id} not found"
                )
            for call in (
                session.query(CallsDBModel)
                .filter_by(phone_id=phone_id)
                .order_by(CallsDBModel.start_time.desc())
                .yield_per(50)
            ):
                # Implemented as a generator to flag the issue that this could yield a huge list
                yield call


class CustomerHandler:
    @classmethod
    def add(cls, name: str, email: str) -> dict:
        with session_scope() as session:
            new_customer = CustomerDBModel(name=name, email=email)
            session.add(new_customer)
            session.flush()
            return dict(new_customer.__dict__)

    @classmethod
    def add_phone(cls, customer_id: int, phone_number: str):
        with session_scope() as session:
            new_phone_number = PhoneDBModel(
                number=phone_number,
                customer_id=customer_id,
            )
            session.add(new_phone_number)
            session.flush()
            return dict(new_phone_number.__dict__)
