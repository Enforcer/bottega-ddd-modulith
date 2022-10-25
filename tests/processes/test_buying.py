from typing import Any, Iterator
from uuid import uuid4

import pytest
from mockito import verify, verifyNoMoreInteractions

from used_stuff_market.availability import Availability
from used_stuff_market.db import ScopedSession
from used_stuff_market.negotiations.events import PriceAgreed
from used_stuff_market.payments import Payments
from used_stuff_market.payments.events import PaymentFinalized
from used_stuff_market.processes.buying import pm
from used_stuff_market.processes.buying.events import PaymentTimeout
from used_stuff_market.shared_kernel.event_bus import EventBus
from used_stuff_market.shared_kernel.money import Currency, Money


@pytest.fixture()
def event_bus() -> EventBus:
    bus = EventBus()
    pm.subscribe(bus)
    return bus


@pytest.fixture(autouse=True)
def reset_session() -> Iterator[None]:
    yield
    ScopedSession().rollback()


item_ids = iter(range(1, 10_000))


@pytest.fixture()
def item_id() -> int:
    return next(item_ids)


def test_initializes_new_payment_after_price_was_agreed_on(
    when: Any,
    event_bus: EventBus,
    item_id: int,
) -> None:
    payment_id = uuid4()
    when(pm.PaymentIdGenerator).generate().thenReturn(payment_id)
    when(Payments).initialize(...)
    price_agreed = PriceAgreed(
        item_id=item_id,
        price=Money(Currency.from_code("USD"), "10.99"),
        seller=uuid4(),
        buyer=uuid4(),
    )

    event_bus.publish(price_agreed)

    verify(Payments, times=1).initialize(
        uuid=payment_id,
        amount=price_agreed.price,
        owner_id=price_agreed.buyer,
        description=f"Payment for item #{item_id}",
    )
    verifyNoMoreInteractions(Payments)


def test_initializes_new_payment_only_once(
    when: Any, event_bus: EventBus, item_id: int
) -> None:
    when(Payments).initialize(...)
    price_agreed = PriceAgreed(
        item_id=item_id,
        price=Money(Currency.from_code("USD"), "10.99"),
        seller=uuid4(),
        buyer=uuid4(),
    )

    event_bus.publish(price_agreed)
    event_bus.publish(price_agreed)

    verify(Payments, times=1).initialize(...)
    verifyNoMoreInteractions(Payments)


def test_finalizing_payment_unregisters_item(
    when: Any, event_bus: EventBus, item_id: int
) -> None:
    when(Availability).unregister(...)
    payment_id = uuid4()
    when(pm.PaymentIdGenerator).generate().thenReturn(payment_id)
    price_agreed = PriceAgreed(
        item_id=item_id,
        price=Money(Currency.from_code("USD"), "10.99"),
        seller=uuid4(),
        buyer=uuid4(),
    )
    event_bus.publish(price_agreed)

    payment_finalized = PaymentFinalized(payment_id)
    event_bus.publish(payment_finalized)

    verify(Availability, times=1).unregister(resource_id=item_id)
    verifyNoMoreInteractions(Availability)


def test_payment_timeout_unlocks_item_and_cancels_payment(
    when: Any, event_bus: EventBus, item_id: int
) -> None:
    when(Availability).unlock(...)
    when(Payments).cancel(...)
    payment_id = uuid4()
    when(pm.PaymentIdGenerator).generate().thenReturn(payment_id)
    buyer_id = uuid4()
    event_bus.publish(
        PriceAgreed(
            item_id=item_id,
            price=Money(Currency.from_code("USD"), "10.99"),
            seller=uuid4(),
            buyer=buyer_id,
        )
    )

    event_bus.publish(PaymentTimeout(payment_id=payment_id))

    verify(Availability, times=1).unlock(resource_id=item_id, locked_by=buyer_id)
    verifyNoMoreInteractions(Availability)
    verify(Payments).cancel(payment_id=payment_id)
    verifyNoMoreInteractions(Payments)


def test_timeout_after_payment_finalization_is_ignored(
    when: Any, event_bus: EventBus, item_id: int
) -> None:
    when(Availability).unregister(...)
    payment_id = uuid4()
    when(pm.PaymentIdGenerator).generate().thenReturn(payment_id)
    event_bus.publish(
        PriceAgreed(
            item_id=item_id,
            price=Money(Currency.from_code("USD"), "10.99"),
            seller=uuid4(),
            buyer=uuid4(),
        )
    )
    event_bus.publish(PaymentFinalized(payment_id=payment_id))

    event_bus.publish(PaymentTimeout(payment_id=payment_id))

    verify(Availability, times=1).unregister(resource_id=item_id)
    verifyNoMoreInteractions(Availability)
