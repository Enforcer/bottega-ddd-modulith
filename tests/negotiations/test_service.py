from unittest.mock import Mock
from uuid import uuid4

import pytest

from used_stuff_market.negotiations.negotiation_id import NegotiationId
from used_stuff_market.negotiations.service import Negotiations


@pytest.fixture()
def repository() -> Mock:
    return Mock()


@pytest.fixture()
def availability() -> Mock:
    return Mock()


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
    repository.get.return_value = Mock(id=negotiation_id)

    service.accept(negotiation_id=negotiation_id, party=negotiation_id.offeree)

    availability.lock_resource.assert_called_once_with(
        resource_id=negotiation_id.item_id,
        lock_for=negotiation_id.offerer,
    )
