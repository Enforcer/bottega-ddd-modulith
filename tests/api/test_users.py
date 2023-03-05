import pytest

from fastapi.testclient import TestClient


@pytest.mark.skip()
def test_registration(client: TestClient) -> None:
    response = client.post("/users", json={"username": "test", "password": "test"})

    assert response.status_code == 200
