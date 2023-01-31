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


class FeatureObject:
    def __init__(self, app_client: AppClient) -> None:
        self._app_client = app_client


class Users(FeatureObject):
    def register(self, username: str, password: str = "foo") -> None:
        self._app_client.register(username=username, password=password)

    def login(self, username: str, password: str = "foo") -> str:
        return self._app_client.login(username=username, password=password)


class Items(FeatureObject):
    def add(self, title: str, description: str, price: int, as_user: str) -> None:
        self._app_client.add_item(
            title=title, description=description, price=price, user_token=as_user
        )


class Likes(FeatureObject):
    def like(self, item_id: int, as_user: str) -> None:
        self._app_client.like(item_id=item_id, user_token=as_user)

    def get_likers(self, item_id: int, as_user: str) -> list[str]:
        return self._app_client.get_likers(item_id=item_id, user_token=as_user)


class Buying(FeatureObject):
    def buy(self, item_id: int, as_user: str) -> None:
        self._app_client.buy(item_id=item_id, user_token=as_user)


class Payments(FeatureObject):
    def get_pending(self, as_user: str) -> list[dict]:
        return self._app_client.get_pending_payments(user_token=as_user)


class Catalog(FeatureObject):
    def search(self, as_user: str, term: str) -> list[dict]:
        return self._app_client.search(term=term, user_token=as_user)


class Negotiations(FeatureObject):
    def start(
        self, item_id: int, offer: int, as_user: str, expect_to_fail: bool = False
    ) -> None:
        expected_code = 400 if expect_to_fail else 200
        self._app_client.start_negotiation(
            item_id=item_id,
            offer=offer,
            user_token=as_user,
            expected_code=expected_code,
        )

    def list(
        self, item_id: int, as_user: str, expect_to_fail: bool = False
    ) -> list[dict]:
        expected_code = 401 if expect_to_fail else 200
        return self._app_client.get_negotiations(
            item_id=item_id, user_token=as_user, expected_code=expected_code
        )

    def accept(
        self, item_id: int, offer_id: int, as_user: str, expect_to_fail: bool = False
    ) -> None:
        expected_code = 401 if expect_to_fail else 200
        self._app_client.accept_negotiation(
            item_id=item_id,
            offer_id=offer_id,
            user_token=as_user,
            expected_code=expected_code,
        )


@pytest.fixture()
def users(app_client: AppClient) -> Users:
    return Users(app_client)


@pytest.fixture()
def items(app_client: AppClient) -> Items:
    return Items(app_client)


@pytest.fixture()
def likes(app_client: AppClient) -> Likes:
    return Likes(app_client)


@pytest.fixture()
def buying(app_client: AppClient) -> Buying:
    return Buying(app_client)


@pytest.fixture()
def payments(app_client: AppClient) -> Payments:
    return Payments(app_client)


@pytest.fixture()
def catalog(app_client: AppClient) -> Catalog:
    return Catalog(app_client)


@pytest.fixture()
def negotiations(app_client: AppClient) -> Negotiations:
    return Negotiations(app_client)


def delete_user(username: str) -> None:
    from used_stuff_market.db import ScopedSession
    from used_stuff_market.users.models import User

    session = ScopedSession()
    session.query(User).filter(User.username == username).delete()
    session.commit()
    ScopedSession.remove()


def test_buying_liked_item(
    users: Users,
    items: Items,
    catalog: Catalog,
    likes: Likes,
    buying: Buying,
    payments: Payments,
) -> None:
    delete_user("seller")
    delete_user("buyer")
    delete_user("second_buyer")
    users.register(username="seller")
    seller_token = users.login(username="seller")
    items.add(
        title="Super shoes",
        description="Leather shoes, great for winter",
        price=100,
        as_user=seller_token,
    )

    users.register(username="buyer")
    buyer_token = users.login(username="buyer")

    item = catalog.search(term="shoes", as_user=buyer_token)[0]
    assert item["likes"] == 0

    likes.like(item_id=item["id"], as_user=buyer_token)

    item = catalog.search(term="shoes", as_user=buyer_token)[0]
    assert item["likes"] == 1

    item_likers = likes.get_likers(item_id=item["id"], as_user=seller_token)
    assert item_likers == ["buyer"]

    buying.buy(item_id=item["id"], as_user=buyer_token)

    users.register(username="second_buyer")
    second_buyer_token = users.login(username="second_buyer")

    found_items = catalog.search(term="shoes", as_user=second_buyer_token)
    assert len(found_items) == 0

    pending_payments = payments.get_pending(as_user=buyer_token)
    assert len(pending_payments) == 1
    assert pending_payments[0]["amount"] == {"amount": 100, "currency": "USD"}


def test_buying_negotiated_item(
    users: Users,
    items: Items,
    catalog: Catalog,
    likes: Likes,
    buying: Buying,
    negotiations: Negotiations,
    payments: Payments,
) -> None:
    delete_user("seller")
    delete_user("buyer")
    users.register(username="seller")
    seller_token = users.login(username="seller")
    items.add(
        title="Super shoes",
        description="Leather shoes, great for winter",
        price=200,
        as_user=seller_token,
    )

    users.register(username="buyer")
    buyer_token = users.login(username="buyer")

    item = catalog.search(term="shoes", as_user=buyer_token)[0]

    negotiations.start(
        item_id=item["id"], offer=50, as_user=seller_token, expect_to_fail=True
    )

    negotiations.start(item_id=item["id"], offer=50, as_user=buyer_token)

    negotiations.list(item_id=item["id"], as_user=buyer_token, expect_to_fail=True)

    negotiations_list = negotiations.list(item_id=item["id"], as_user=seller_token)
    assert len(negotiations_list) == 1
    offer_id = negotiations_list[0]["id"]

    negotiations.accept(item_id=item["id"], offer_id=offer_id, as_user=seller_token)

    buying.buy(item_id=item["id"], as_user=buyer_token)

    pending_payments = payments.get_pending(as_user=buyer_token)
    assert len(pending_payments) == 1
    assert pending_payments[0]["amount"] == {"amount": 50, "currency": "USD"}
