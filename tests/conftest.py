import pytest

from sqlalchemy import text, create_engine
from used_stuff_market.db import engine, Base, session_factory
from used_stuff_market.availability.models import *  # for models discovery
from used_stuff_market.catalog.models import *


@pytest.fixture(scope="session", autouse=True)
def db_for_tests() -> None:
    test_db_name = engine.url.database + "_tests"

    with engine.connect().execution_options(
        isolation_level="AUTOCOMMIT"
    ) as connection:
        connection.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
        connection.execute(text(f"CREATE DATABASE {test_db_name}"))

    testing_db_url = engine.url.set(database=test_db_name)
    test_db_engine = create_engine(testing_db_url, echo=True)
    session_factory.configure(bind=test_db_engine)

    with test_db_engine.connect().execution_options(
        isolation_level="AUTOCOMMIT"
    ) as connection:
        connection.execute(text(f"CREATE SCHEMA availability"))
        connection.execute(text(f"CREATE SCHEMA catalog"))
        connection.execute(text(f"CREATE SCHEMA items"))
        connection.execute(text(f"CREATE SCHEMA payments"))

    Base.metadata.create_all(bind=test_db_engine)
    yield
    test_db_engine.dispose()
