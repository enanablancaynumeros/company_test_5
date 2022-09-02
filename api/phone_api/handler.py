from .db_connection import session_scope
from .schemas import Call


class CallsHandler:
    @classmethod
    def save_user_call(cls, call: Call) -> int:
        with session_scope() as session:
            from .data_models import CallsDBModel, PhoneDBModel

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
            from .data_models import CallsDBModel

            for call in (
                session.query(CallsDBModel)
                .filter_by(phone_id=phone_id)
                .order_by(CallsDBModel.start_time.desc())
                .yield_per(50)
            ):
                yield call
