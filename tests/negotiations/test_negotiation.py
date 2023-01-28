from uuid import uuid4

import pytest

from used_stuff_market.negotiations.negotiation import Negotiation
from used_stuff_market.shared_kernel.money import Currency, Money


@pytest.mark.skip()
def test_negotiation() -> None:
    owner = uuid4()
    negotiation = Negotiation(  # noqa
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=uuid4(),
        offeree=owner,
    )

    ...
