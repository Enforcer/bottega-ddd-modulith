import pytest

from tests.negotiations.test_negotiation import NegotiationFactory
from used_stuff_market import db
from used_stuff_market.negotiations.negotiation_repository import NegotiationRepository


@pytest.fixture
def repository():
    return NegotiationRepository(collection=db.mongo_db["negotiations"])


def test_detects_duplicates(repository) -> None:
    negotiation = NegotiationFactory()

    repository.create(negotiation)
    with pytest.raises(repository.AlreadyExists):
        repository.create(negotiation)
