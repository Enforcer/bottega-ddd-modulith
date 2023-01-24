import pytest
from fastapi.testclient import TestClient

from tests.acceptance.steps import Steps


@pytest.fixture()
def steps(client: TestClient) -> Steps:
    return Steps(client)
