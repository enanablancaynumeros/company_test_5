from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy_utils import EmailType

from .db_connection import BaseDBModel


class BaseDatesDBMixin:
    created = Column(
        DateTime, default=lambda: datetime.utcnow(), nullable=False
    )  # noqa: W0108
    updated = Column(
        DateTime, onupdate=lambda: datetime.utcnow(), nullable=True
    )  # noqa: W0108


class BaseDBMixin(BaseDatesDBMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)


class CustomerDBModel(BaseDBModel, BaseDBMixin):
    __tablename__ = "customers"

    name = Column(String(255), nullable=False)
    email = Column(EmailType, unique=True, nullable=False)


class PhoneDBModel(BaseDBModel, BaseDBMixin):
    __tablename__ = "phones"

    number = Column(String(15), nullable=False)
    customer_id = Column(
        Integer,
        ForeignKey("customers.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )


class CallsDBModel(BaseDBModel, BaseDBMixin):
    __tablename__ = "calls"

    duration_in_minutes = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    target_number = Column(String(15), nullable=False)
    phone_id = Column(
        Integer,
        ForeignKey("phones.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )


class InvoicesDBModel(BaseDBModel, BaseDBMixin):
    __tablename__ = "invoices"

    phone_id = Column(
        Integer,
        ForeignKey("phones.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    invoice_sent = Column(Date, nullable=True)
    month_invoice = Column(Date, nullable=False)
