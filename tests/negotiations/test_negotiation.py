from uuid import UUID, uuid4

import pytest

from used_stuff_market.negotiations.negotiation import (
    CannotAcceptOwnOffer,
    CannotCounterOwnOffer,
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
        item_id=-1,
        owner=offeree,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=offerer,
        offeree=offeree,
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


def test_offerer_accepts_counter_offer(
    negotiation: Negotiation, offerer: UUID, offeree: UUID
) -> None:
    negotiation.propose_counter_offer(
        party=offeree, counter_offer=Money(Currency.from_code("USD"), "19.99")
    )

    negotiation.accept_offer(party=offerer)

    assert negotiation.offer == Money(Currency.from_code("USD"), "19.99")


def test_cannot_counter_offer_on_accepted_negotiation(
    negotiation: Negotiation, offeree: UUID
) -> None:
    negotiation.accept_offer(party=offeree)

    with pytest.raises(NegotiationClosed):
        negotiation.propose_counter_offer(
            party=offeree, counter_offer=Money(Currency.from_code("USD"), "19.99")
        )


def test_offerer_rejects_counter_offer(
    negotiation: Negotiation, offerer: UUID, offeree: UUID
) -> None:
    negotiation.propose_counter_offer(
        party=offeree, counter_offer=Money(Currency.from_code("USD"), "19.99")
    )

    negotiation.reject_offer(party=offerer)

    assert negotiation.offer == Money(Currency.from_code("USD"), "19.99")


def test_cannot_counter_offer_on_rejected_negotiation(
    negotiation: Negotiation, offeree: UUID
) -> None:
    negotiation.reject_offer(party=offeree)

    with pytest.raises(NegotiationClosed):
        negotiation.propose_counter_offer(
            party=offeree, counter_offer=Money(Currency.from_code("USD"), "19.99")
        )


def test_cannot_counter_own_offer(negotiation: Negotiation, offerer: UUID) -> None:
    with pytest.raises(CannotCounterOwnOffer):
        negotiation.propose_counter_offer(
            party=offerer, counter_offer=Money(Currency.from_code("USD"), "19.99")
        )


def test_cannot_accept_own_counter_offer(
    negotiation: Negotiation, offeree: UUID
) -> None:
    negotiation.propose_counter_offer(
        party=offeree, counter_offer=Money(Currency.from_code("USD"), "10.99")
    )
    with pytest.raises(CannotAcceptOwnOffer):
        negotiation.accept_offer(party=offeree)


def test_cannot_reject_own_counter_offer(
    negotiation: Negotiation, offeree: UUID
) -> None:
    negotiation.propose_counter_offer(
        party=offeree, counter_offer=Money(Currency.from_code("USD"), "10.99")
    )
    with pytest.raises(CannotRejectOwnOffer):
        negotiation.reject_offer(party=offeree)


def test_counter_offers_counter_offer(
    negotiation: Negotiation, offerer: UUID, offeree: UUID
) -> None:
    negotiation.propose_counter_offer(
        party=offeree, counter_offer=Money(Currency.from_code("USD"), "19.99")
    )
    negotiation.propose_counter_offer(
        party=offerer, counter_offer=Money(Currency.from_code("USD"), "12.99")
    )
    negotiation.propose_counter_offer(
        party=offeree, counter_offer=Money(Currency.from_code("USD"), "17.99")
    )
    negotiation.propose_counter_offer(
        party=offerer, counter_offer=Money(Currency.from_code("USD"), "15.99")
    )

    negotiation.accept_offer(party=offeree)
    assert negotiation.offer == Money(Currency.from_code("USD"), "15.99")
