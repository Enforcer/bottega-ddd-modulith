from fastapi.testclient import TestClient


def test_buying_liked_item(client: TestClient) -> None:
    register_response = client.post(
        "/users", json={"username": "seller", "password": "foo"}
    )
    assert register_response.status_code == 200, register_response.json()
    login_response = client.post(
        "/users/login", json={"username": "seller", "password": "foo"}
    )
    assert login_response.status_code == 200, login_response.json()
    seller_token = login_response.json()["token"]

    add_item_response = client.post(
        "/items",
        headers={"User-Id": seller_token},
        json={
            "title": "Super shoes",
            "description": "Leather shoes, great for winter",
            "starting_price": {"amount": 100, "currency": "USD"},
        },
    )
    assert add_item_response.status_code == 204, add_item_response.text

    register_response = client.post(
        "/users", json={"username": "buyer", "password": "foo"}
    )
    assert register_response.status_code == 200, register_response.json()
    login_response = client.post(
        "/users/login", json={"username": "buyer", "password": "foo"}
    )
    assert login_response.status_code == 200, login_response.json()
    buyer_token = login_response.json()["token"]

    term = "shoes"
    search_response = client.get(
        f"/catalog/search/{term}", headers={"User-Id": buyer_token}
    )
    assert search_response.status_code == 200, search_response.json()
    item = search_response.json()[0]
    assert item["likes"] == 0

    like_response = client.post(
        f"/items/{item['id']}/like", headers={"User-Id": buyer_token}
    )
    assert like_response.status_code == 200, like_response.json()

    search_response = client.get(
        f"/catalog/search/{term}", headers={"User-Id": buyer_token}
    )
    assert search_response.status_code == 200, search_response.json()
    item = search_response.json()[0]
    assert item["likes"] == 1

    item_likers = client.get(
        f"/items/{item['id']}/likers", headers={"User-Id": seller_token}
    )
    assert item_likers.status_code == 200, item_likers.json()
    assert item_likers.json() == ["buyer"]

    buy_response = client.post(
        f"/items/{item['id']}/buy", headers={"User-Id": buyer_token}
    )
    assert buy_response.status_code == 200, buy_response.json()

    register_response = client.post(
        "/users", json={"username": "second_buyer", "password": "foo"}
    )
    assert register_response.status_code == 200, register_response.json()
    login_response = client.post(
        "/users/login", json={"username": "second_buyer", "password": "foo"}
    )
    assert login_response.status_code == 200, login_response.json()
    second_buyer_token = login_response.json()["token"]

    search_response = client.get(
        f"/catalog/search/{term}", headers={"User-Id": second_buyer_token}
    )
    assert search_response.status_code == 200, search_response.json()
    assert len(search_response.json()) == 0

    pending_payments_response = client.get(
        "/payments/pending", headers={"User-Id": buyer_token}
    )
    assert (
        pending_payments_response.status_code == 200
    ), pending_payments_response.json()
    assert len(pending_payments_response.json()) == 1
    pending_payment = pending_payments_response.json()[0]
    assert pending_payment["amount"] == {"amount": 100, "currency": "USD"}


def test_buying_negotiated_item(client: TestClient) -> None:
    register_response = client.post(
        "/users", json={"username": "seller2", "password": "foo"}
    )
    assert register_response.status_code == 200, register_response.json()
    login_response = client.post(
        "/users/login", json={"username": "seller2", "password": "foo"}
    )
    assert login_response.status_code == 200, login_response.json()
    seller_token = login_response.json()["token"]

    add_item_response = client.post(
        "/items",
        headers={"User-Id": seller_token},
        json={
            "title": "Super shoes",
            "description": "Leather shoes, great for winter",
            "starting_price": {"amount": 200, "currency": "USD"},
        },
    )
    assert add_item_response.status_code == 204, add_item_response.text

    register_response = client.post(
        "/users", json={"username": "buyer2", "password": "foo"}
    )
    assert register_response.status_code == 200, register_response.json()
    login_response = client.post(
        "/users/login", json={"username": "buyer2", "password": "foo"}
    )
    assert login_response.status_code == 200, login_response.json()
    buyer_token = login_response.json()["token"]

    term = "shoes"
    search_response = client.get(
        f"/catalog/search/{term}", headers={"User-Id": buyer_token}
    )
    assert search_response.status_code == 200, search_response.json()
    item = search_response.json()[0]

    start_negotiation_response = client.post(
        f"/items/{item['id']}/offer",
        headers={"User-Id": seller_token},
        json={"amount": 50, "currency": "USD"},
    )
    assert (
        start_negotiation_response.status_code == 400
    ), start_negotiation_response.text

    start_negotiation_response = client.post(
        f"/items/{item['id']}/offer",
        headers={"User-Id": buyer_token},
        json={"amount": 50, "currency": "USD"},
    )
    assert (
        start_negotiation_response.status_code == 200
    ), start_negotiation_response.json()

    negotiation_offers_response = client.get(
        f"/items/{item['id']}/offers", headers={"User-Id": buyer_token}
    )
    assert (
        negotiation_offers_response.status_code == 401
    ), negotiation_offers_response.json()

    negotiation_offers_response = client.get(
        f"/items/{item['id']}/offers", headers={"User-Id": seller_token}
    )
    assert (
        negotiation_offers_response.status_code == 200
    ), negotiation_offers_response.json()
    assert len(negotiation_offers_response.json()) == 1
    offer_id = negotiation_offers_response.json()[0]["id"]

    accept_offer_response = client.post(
        f"/items/{item['id']}/offers/{offer_id}/accept",
        headers={"User-Id": seller_token},
    )
    assert accept_offer_response.status_code == 200, accept_offer_response.json()

    buy_response = client.post(
        f"/items/{item['id']}/buy", headers={"User-Id": buyer_token}
    )
    assert buy_response.status_code == 200, buy_response.json()

    pending_payments_response = client.get(
        "/payments/pending", headers={"User-Id": buyer_token}
    )
    assert (
        pending_payments_response.status_code == 200
    ), pending_payments_response.json()
    assert len(pending_payments_response.json()) == 1
    pending_payment = pending_payments_response.json()[0]
    assert pending_payment["amount"] == {"amount": 50, "currency": "USD"}
