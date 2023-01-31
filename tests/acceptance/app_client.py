from fastapi.testclient import TestClient


class AppClient:
    def __init__(self, test_client: TestClient) -> None:
        self._test_client = test_client

    def register(self, username: str, password: str = "foo") -> None:
        response = self._test_client.post(
            "/users", json={"username": username, "password": password}
        )
        assert response.status_code == 200, response.json()

    def login(self, username: str, password: str = "foo") -> str:
        response = self._test_client.post(
            "/users/login", json={"username": username, "password": password}
        )
        assert response.status_code == 200, response.json()
        return response.json()["token"]

    def add_item(
        self, title: str, description: str, price: int, user_token: str
    ) -> None:
        response = self._test_client.post(
            "/items",
            json={
                "title": title,
                "description": description,
                "starting_price": {"amount": price, "currency": "USD"},
            },
            headers={"User-Id": user_token},
        )
        assert response.status_code == 204, response.json()

    def search(self, term: str, user_token: str) -> list[dict]:
        response = self._test_client.get(
            f"/catalog/search/{term}",
            headers={"User-Id": user_token},
        )
        assert response.status_code == 200, response.json()
        return response.json()

    def like(self, item_id: int, user_token: str) -> None:
        response = self._test_client.post(
            f"/items/{item_id}/like",
            headers={"User-Id": user_token},
        )
        assert response.status_code == 200, response.json()

    def get_likers(self, item_id: int, user_token: str) -> list[str]:
        response = self._test_client.get(
            f"/items/{item_id}/likers",
            headers={"User-Id": user_token},
        )
        assert response.status_code == 200, response.json()
        return response.json()

    def buy(self, item_id: int, user_token: str) -> None:
        response = self._test_client.post(
            f"/items/{item_id}/buy",
            headers={"User-Id": user_token},
        )
        assert response.status_code == 200, response.json()

    def get_pending_payments(self, user_token: str) -> list[dict]:
        response = self._test_client.get(
            "/payments/pending", headers={"User-Id": user_token}
        )
        assert response.status_code == 200, response.json()
        return response.json()

    def start_negotiation(
        self, item_id: int, offer: int, user_token: str, expected_code: int = 200
    ) -> None:
        response = self._test_client.post(
            f"/items/{item_id}/offer",
            json={"amount": offer, "currency": "USD"},
            headers={"User-Id": user_token},
        )
        assert response.status_code == expected_code, response.json()

    def get_negotiations(
        self, item_id: int, user_token: str, expected_code: int = 200
    ) -> list[dict]:
        response = self._test_client.get(
            f"/items/{item_id}/offers", headers={"User-Id": user_token}
        )
        assert response.status_code == expected_code, response.json()
        return response.json()

    def accept_negotiation(
        self, item_id: int, offer_id: int, user_token: str, expected_code: int = 200
    ) -> None:
        response = self._test_client.post(
            f"/items/{item_id}/offers/{offer_id}/accept",
            headers={"User-Id": user_token},
        )
        assert response.status_code == expected_code, response.json()
