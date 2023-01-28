from unittest.mock import Mock, seal
from uuid import uuid4

import pytest

from used_stuff_market.availability import Availability
from used_stuff_market.negotiations.negotiation import Negotiation
from used_stuff_market.negotiations.negotiation_id import NegotiationId
from used_stuff_market.negotiations.repository import NegotiationsRepository
from used_stuff_market.negotiations.service import Negotiations
from used_stuff_market.shared_kernel.money import USD, Money


@pytest.fixture()
def repository() -> Mock:
    return Mock(spec_set=NegotiationsRepository)


@pytest.fixture()
def availability() -> Mock:
    return Mock(spec_set=Availability)


@pytest.fixture()
def service(availability: Mock, repository: Mock) -> Negotiations:
    return Negotiations(
        availability=availability,
        repository=repository,
    )


def test_accepting_negotiation_locks_the_item(
    service: Negotiations, repository: Mock, availability: Mock
) -> None:
    negotiation_id = NegotiationId(item_id=-2, offerer=uuid4(), offeree=uuid4())
    repository.get.return_value = Negotiation(
        item_id=2,
        owner=negotiation_id.offeree,
        offer=Money(USD, "9.99"),
        offerer=negotiation_id.offerer,
        offeree=negotiation_id.offeree,
    )
    seal(repository)
    availability.lock = Mock(return_value=None)
    seal(availability)

    service.accept(negotiation_id=negotiation_id, party=negotiation_id.offeree)

    availability.lock.assert_called_once_with(
        resource_id=negotiation_id.item_id,
        lock_for=negotiation_id.offerer,
    )
