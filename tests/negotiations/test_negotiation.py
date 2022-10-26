from uuid import uuid4

import pytest

from used_stuff_market.negotiations.negotiation import Negotiation
from used_stuff_market.shared_kernel.money import Currency, Money


@pytest.mark.skip()
def test_negotiation() -> None:
    negotiation = Negotiation(  # noqa
        offer=Money(Currency.from_code("USD"), "9.99"), offerer=uuid4(), offeree=uuid4()
    )

    ...
