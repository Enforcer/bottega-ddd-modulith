import os
import pathlib
from typing import Iterator

import alembic.command
import alembic.config
import pytest
from _pytest.tmpdir import TempPathFactory
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from used_stuff_market.api.app import app
from used_stuff_market.db import Base, session_factory


@pytest.fixture(scope="session", autouse=True)
def db_for_tests(tmp_path_factory: TempPathFactory) -> Iterator[None]:
    tmp_dir = tmp_path_factory.mktemp("db_for_tests")
    test_db_file = tmp_dir / "test_db.sqlite"

    test_db_engine = create_engine(f"sqlite:///{test_db_file}", echo=True)
    session_factory.configure(bind=test_db_engine)

    os.environ["CONFIG_DB_URL"] = str(test_db_engine.url)
    Base.metadata.create_all(test_db_engine)
    yield
    test_db_engine.dispose()


@pytest.fixture()
def client() -> Iterator[TestClient]:
    with TestClient(app) as _client:
        yield _client
