import contextlib
import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import create_database

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@"
    f"{os.environ['POSTGRES_HOST']}/{os.environ['POSTGRES_DB']}"
)

db_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    client_encoding="utf8",
    isolation_level="SERIALIZABLE",
    poolclass=NullPool,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

BaseDBModel = declarative_base()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def create_db_if_not_exists():
    with contextlib.suppress(ProgrammingError):
        create_database(SQLALCHEMY_DATABASE_URL)


def recreate_postgres_metadata():
    from api.phone_api.alembic.utils import (alembic_downgrade_base,
                                             alembic_upgrade_head)

    create_db_if_not_exists()
    alembic_downgrade_base()
    alembic_upgrade_head()
