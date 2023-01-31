import pytest

from tests.acceptance.features import (
    Buying,
    Catalog,
    Items,
    Likes,
    Negotiations,
    Payments,
    Users,
)


def delete_user(username: str) -> None:
    from used_stuff_market.db import ScopedSession
    from used_stuff_market.users.models import User

    session = ScopedSession()
    session.query(User).filter(User.username == username).delete()
    session.commit()
    ScopedSession.remove()


@pytest.fixture()
def seller_token(users: Users) -> str:
    users.register(username="seller")
    yield users.login(username="seller")
    delete_user("seller")


@pytest.fixture()
def buyer_token(users: Users) -> str:
    users.register(username="buyer")
    yield users.login(username="buyer")
    delete_user("buyer")


def test_buying_liked_item(
    users: Users,
    items: Items,
    catalog: Catalog,
    likes: Likes,
    buying: Buying,
    payments: Payments,
    seller_token: str,
    buyer_token: str,
) -> None:
    items.add(
        title="Super shoes",
        description="Leather shoes, great for winter",
        price=100,
        as_user=seller_token,
    )

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
    request: pytest.FixtureRequest,
) -> None:
    users.register(username="seller")
    request.addfinalizer(lambda: delete_user("seller"))
    seller_token = users.login(username="seller")
    items.add(
        title="Super shoes",
        description="Leather shoes, great for winter",
        price=200,
        as_user=seller_token,
    )

    users.register(username="buyer")
    request.addfinalizer(lambda: delete_user("buyer"))
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
