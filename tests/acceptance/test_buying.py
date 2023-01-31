import pytest
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


@pytest.fixture()
def app_client(client: TestClient) -> AppClient:
    return AppClient(client)


def delete_user(username: str) -> None:
    from used_stuff_market.db import ScopedSession
    from used_stuff_market.users.models import User

    session = ScopedSession()
    session.query(User).filter(User.username == username).delete()
    session.commit()
    ScopedSession.remove()


def test_buying_liked_item(app_client: AppClient) -> None:
    delete_user("seller")
    delete_user("buyer")
    delete_user("second_buyer")
    app_client.register(username="seller")
    seller_token = app_client.login(username="seller")
    app_client.add_item(
        title="Super shoes",
        description="Leather shoes, great for winter",
        price=100,
        user_token=seller_token,
    )

    app_client.register(username="buyer")
    buyer_token = app_client.login(username="buyer")

    item = app_client.search(term="shoes", user_token=buyer_token)[0]
    assert item["likes"] == 0

    app_client.like(item_id=item["id"], user_token=buyer_token)

    item = app_client.search(term="shoes", user_token=buyer_token)[0]
    assert item["likes"] == 1

    item_likers = app_client.get_likers(item_id=item["id"], user_token=seller_token)
    assert item_likers == ["buyer"]

    app_client.buy(item_id=item["id"], user_token=buyer_token)

    app_client.register(username="second_buyer")
    second_buyer_token = app_client.login(username="second_buyer")

    found_items = app_client.search(term="shoes", user_token=second_buyer_token)
    assert len(found_items) == 0

    pending_payments = app_client.get_pending_payments(user_token=buyer_token)
    assert len(pending_payments) == 1
    assert pending_payments[0]["amount"] == {"amount": 100, "currency": "USD"}


def test_buying_negotiated_item(app_client: AppClient) -> None:
    delete_user("seller")
    delete_user("buyer")
    app_client.register(username="seller")
    seller_token = app_client.login(username="seller")

    app_client.add_item(
        title="Super shoes",
        description="Leather shoes, great for winter",
        price=200,
        user_token=seller_token,
    )

    app_client.register(username="buyer")
    buyer_token = app_client.login(username="buyer")

    item = app_client.search(term="shoes", user_token=buyer_token)[0]

    app_client.start_negotiation(
        item_id=item["id"], offer=50, user_token=seller_token, expected_code=400
    )

    app_client.start_negotiation(item_id=item["id"], offer=50, user_token=buyer_token)

    app_client.get_negotiations(
        item_id=item["id"], user_token=buyer_token, expected_code=401
    )

    negotiations = app_client.get_negotiations(
        item_id=item["id"], user_token=seller_token
    )
    assert len(negotiations) == 1
    offer_id = negotiations[0]["id"]

    app_client.accept_negotiation(
        item_id=item["id"], offer_id=offer_id, user_token=seller_token
    )

    app_client.buy(item_id=item["id"], user_token=buyer_token)

    pending_payments = app_client.get_pending_payments(user_token=buyer_token)
    assert len(pending_payments) == 1
    assert pending_payments[0]["amount"] == {"amount": 50, "currency": "USD"}
