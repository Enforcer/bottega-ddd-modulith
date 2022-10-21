import pathlib
import os

import pytest

import alembic.command
import alembic.config
from sqlalchemy import text, create_engine
from used_stuff_market.db import engine, session_factory


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

    os.environ["CONFIG_DB_URL"] = str(testing_db_url)
    script_location = (
        pathlib.Path(__file__).parent.parent / "used_stuff_market/db/migrations/"
    )
    config = alembic.config.Config()
    config.set_main_option("script_location", str(script_location))
    alembic.command.upgrade(config=config, revision="head")
    yield
    test_db_engine.dispose()
