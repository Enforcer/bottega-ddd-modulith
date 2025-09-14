from unittest.mock import patch, Mock

import pytest
from uuid import uuid4
from typing import Iterator

from lagom import Container

from used_stuff_market.availability import Availability
from used_stuff_market.items import Items
from used_stuff_market.main.container import manage_session
from used_stuff_market.orders import Orders, DeliveryMethod
from used_stuff_market.orders.address import Address
from used_stuff_market.shared_kernel.money import Money, Currency


@pytest.fixture()
def orders(container: Container) -> Iterator[Orders]:
    with manage_session(container) as container_with_session:
        yield container_with_session.resolve(Orders)


@patch.object(
    Items, "get_item_price", return_value=Money(Currency.from_code("PLN"), "100")
)
@patch.object(Availability, "lock")
def test_newly_placed_order_awaits_payment(
    _availability_mock: Mock, _items_mock: Mock, orders: Orders
) -> None:
    owner_id = uuid4()
    item_id = 123
    address = Address(
        line_1="Privet Drive 4",
        line_2=None,
        postal_code="12345",
        city="Little Whinging",
        country_code="PL",
    )
    orders.place(owner_id, item_id, DeliveryMethod.COURIER, address)

    pending_orders = orders.get_pending_orders(owner_id)

    assert len(pending_orders) == 1
    assert pending_orders[0].paid_at is None
    assert pending_orders[0].shipped_at is None
