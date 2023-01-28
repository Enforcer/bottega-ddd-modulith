from typing import Any
from uuid import uuid4

import pytest
from mockito import mock, verify

from used_stuff_market.availability import Availability
from used_stuff_market.negotiations.negotiation import Negotiation
from used_stuff_market.negotiations.repository import NegotiationsRepository
from used_stuff_market.negotiations.service import Negotiations
from used_stuff_market.shared_kernel.money import USD, Money


@pytest.fixture()
def repository() -> Any:
    return mock(NegotiationsRepository)


@pytest.fixture()
def availability() -> Any:
    return mock(Availability)


@pytest.fixture()
def service(availability: Any, repository: Any) -> Negotiations:
    return Negotiations(
        availability=availability,
        repository=repository,
    )


def test_accepting_negotiation_locks_the_item(
    service: Negotiations, repository: Any, availability: Any, when: Any
) -> None:
    owner = uuid4()
    negotiation = Negotiation(
        item_id=2,
        owner=owner,
        offer=Money(USD, "9.99"),
        offerer=uuid4(),
        offeree=owner,
    )
    when(repository).get(negotiation.id).thenReturn(negotiation)
    when(availability).lock(...).thenReturn(None)

    service.accept(negotiation_id=negotiation.id, party=negotiation.id.offeree)

    verify(availability, times=1).lock(
        resource_id=negotiation.id.item_id,
        lock_for=negotiation.id.offerer,
    )
