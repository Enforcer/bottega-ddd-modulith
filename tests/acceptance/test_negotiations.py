from decimal import Decimal

import pytest
from attr import define
from fastapi.testclient import TestClient

SELLER_ID = 1
BUYER_ID = 2


@define
class Steps:
    _client: TestClient

    def start_negotiation(
        self,
        item_id: int,
        user_id: int,
        seller_id: int,
        buyer_id: int,
        price: Decimal,
        currency: str,
    ) -> None:
        response = self._client.post(
            f"/items/{item_id}/negotiations",
            json={
                "seller_id": seller_id,
                "buyer_id": buyer_id,
                "price": str(price),
                "currency": currency,
            },
            headers={"user-id": str(user_id)},
        )
        assert response.status_code == 204, (response.status_code, response.json())

    def get_negotiation(
        self, item_id: int, user_id: int, seller_id: int, buyer_id: int
    ) -> dict:
        response = self._client.get(
            f"/items/{item_id}/negotiations",
            params={
                "seller_id": seller_id,
                "buyer_id": buyer_id,
            },
            headers={"user-id": str(user_id)},
        )
        assert response.status_code == 200
        return response.json()

    def accept_negotiation(
        self, item_id: int, user_id: int, seller_id: int, buyer_id: int
    ) -> None:
        response = self._client.post(
            f"/items/{item_id}/negotiations/accept",
            json={
                "seller_id": seller_id,
                "buyer_id": buyer_id,
            },
            headers={"user-id": str(user_id)},
        )
        assert response.status_code == 204, (response.status_code, response.json())


def test_accepting_negotiation(steps: Steps) -> None:
    steps.start_negotiation(
        item_id=1,
        user_id=BUYER_ID,
        seller_id=SELLER_ID,
        buyer_id=BUYER_ID,
        price=Decimal("1.99"),
        currency="USD",
    )
    steps.accept_negotiation(
        item_id=1, user_id=SELLER_ID, seller_id=SELLER_ID, buyer_id=BUYER_ID
    )

    negotiation = steps.get_negotiation(
        item_id=1, user_id=BUYER_ID, seller_id=SELLER_ID, buyer_id=BUYER_ID
    )
    assert negotiation["state"] == "accepted"


@pytest.fixture()
def steps(client: TestClient) -> Steps:
    return Steps(client)
