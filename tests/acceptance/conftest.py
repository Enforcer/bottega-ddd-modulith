import pytest
from fastapi.testclient import TestClient

from tests.acceptance.steps import Steps
from used_stuff_market.api.app import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture()
def steps(client: TestClient) -> Steps:
    return Steps(client)
