from decimal import Decimal

import pytest

from tests.negotiations.factories import SELLER_ID
from tests.negotiations.test_negotiation import NegotiationFactory
from used_stuff_market import db
from used_stuff_market.db import migrate_mongo_db
from used_stuff_market.negotiations.negotiation_repository import NegotiationRepository


@pytest.fixture(autouse=True)
def setup_db():
    db.mongo_db.drop_collection("negotiations")
    migrate_mongo_db()


@pytest.fixture
def repository():
    return NegotiationRepository(collection=db.mongo_db["negotiations"])


def test_detects_duplicates(repository) -> None:
    negotiation = NegotiationFactory()

    repository.create(negotiation)
    with pytest.raises(repository.AlreadyExists):
        repository.create(negotiation)


def test_detects_stale_version(repository) -> None:
    negotiation = NegotiationFactory()
    repository.create(negotiation)

    read_negotiation = repository.get(*negotiation.id)
    read_negotiation.counteroffer(user_id=SELLER_ID, price=Decimal(12), currency="USD")
    repository.update(read_negotiation)

    with pytest.raises(repository.StaleVersion):
        repository.update(read_negotiation)
