from uuid import UUID, uuid4

import pytest

from used_stuff_market.negotiations.negotiation import (
    CannotAcceptOwnOffer,
    CannotRejectOwnOffer,
    Negotiation,
    NegotiationClosed,
)
from used_stuff_market.shared_kernel.money import Currency, Money


@pytest.fixture()
def offerer() -> UUID:
    return uuid4()


@pytest.fixture()
def offeree() -> UUID:
    return uuid4()


@pytest.fixture()
def negotiation(offerer: UUID, offeree: UUID) -> Negotiation:
    return Negotiation(  # noqa
        offer=Money(Currency.from_code("USD"), "9.99"), offerer=offerer, offeree=offeree
    )


def test_cannot_reject_accepted_negotiation(
    negotiation: Negotiation, offeree: UUID
) -> None:
    negotiation.accept_offer(party=offeree)
    with pytest.raises(NegotiationClosed):
        negotiation.reject_offer(party=offeree)


def test_cannot_accept_accepted_negotiation(
    negotiation: Negotiation, offeree: UUID
) -> None:
    negotiation.accept_offer(party=offeree)
    with pytest.raises(NegotiationClosed):
        negotiation.accept_offer(party=offeree)


def test_cannot_accept_offer_as_offerer(
    negotiation: Negotiation, offerer: UUID
) -> None:
    with pytest.raises(CannotAcceptOwnOffer):
        negotiation.accept_offer(party=offerer)


def test_cannot_reject_offer_as_offerer(
    negotiation: Negotiation, offerer: UUID
) -> None:
    with pytest.raises(CannotRejectOwnOffer):
        negotiation.reject_offer(party=offerer)
