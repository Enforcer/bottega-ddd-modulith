from fastapi.testclient import TestClient


def test_registration(client: TestClient) -> None:
    response = client.post("/users", json={"username": "test", "password": "test"})

    assert response.status_code == 200
