from uuid import uuid4

import pytest

from used_stuff_market.availability import Availability
from used_stuff_market.negotiations.negotiation_id import NegotiationId
from used_stuff_market.negotiations.repository import NegotiationsRepository
from used_stuff_market.negotiations.service import Negotiations
from used_stuff_market.shared_kernel.money import USD, Money


@pytest.fixture()
def availability() -> Availability:
    return Availability()


@pytest.fixture()
def negotiations(availability: Availability) -> Negotiations:
    return Negotiations(
        availability=availability,
        repository=NegotiationsRepository(),
    )


def test_cannot_lock_item_that_was_negotiated(
    availability: Availability, negotiations: Negotiations
) -> None:
    owner_id = uuid4()
    item_id = -3
    availability.register(resource_id=item_id, owner_id=owner_id)
    buyer = uuid4()
    negotiations.start(
        item_id=item_id,
        owner=owner_id,
        offerer=buyer,
        offeree=owner_id,
        offer=Money(USD, 100),
    )

    negotiations.accept(
        negotiation_id=NegotiationId(item_id=item_id, offerer=buyer, offeree=owner_id),
        party=owner_id,
    )

    with pytest.raises(Availability.AlreadyLocked):
        availability.lock(resource_id=item_id, lock_for=uuid4())
