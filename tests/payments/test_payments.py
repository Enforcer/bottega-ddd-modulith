from uuid import uuid4

import pytest

from used_stuff_market.payments import Payments
from used_stuff_market.utils import Currency, Money


def test_initialized_payment_returned_on_pending_list(payments: Payments) -> None:
    owner_id = uuid4()
    payments.initialize(
        owner_id=owner_id,
        uuid=uuid4(),
        amount=Money(Currency.from_code("USD"), "10.99"),
        description="For order #123",
    )

    pending = payments.pending(owner_id=owner_id)

    assert len(pending) == 1


def test_finalized_payment_does_not_appear_on_pending_list(payments: Payments) -> None:
    owner_id = uuid4()
    payment_uuid = uuid4()
    payments.initialize(
        owner_id=owner_id,
        uuid=payment_uuid,
        amount=Money(Currency.from_code("USD"), "10.99"),
        description="For order #321",
    )

    payments.finalize(owner_id=owner_id, uuid=payment_uuid)

    pending = payments.pending(owner_id=owner_id)
    assert len(pending) == 0


@pytest.fixture()
def payments() -> Payments:
    return Payments()
