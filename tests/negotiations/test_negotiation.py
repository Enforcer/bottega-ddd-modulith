from typing import cast
from uuid import UUID, uuid4

import factory
import pytest
from _pytest.fixtures import SubRequest

from used_stuff_market.negotiations.negotiation import (
    Negotiation,
    NegotiationClosed,
    Resolution,
    WaitingForOtherSide,
)
from used_stuff_market.shared_kernel.money import Currency, Money


@pytest.fixture()
def offeree() -> UUID:
    return uuid4()


@pytest.fixture()
def offerer() -> UUID:
    return uuid4()


@pytest.fixture(params=["offeree", "offerer"])
def owner(request: SubRequest) -> UUID:
    value = request.getfixturevalue(request.param)
    return cast(UUID, value)


class NegotiationFactory(factory.Factory):
    class Meta:
        model = Negotiation

    item_id = factory.Sequence(lambda n: n)
    offer = Money(Currency.from_code("USD"), "9.99")


@pytest.fixture()
def negotiation(owner: UUID, offerer: UUID, offeree: UUID) -> Negotiation:
    return NegotiationFactory(owner=owner, offerer=offerer, offeree=offeree)


def test_accepted_negotiation_has_accepted_resolution(
    offeree: UUID, negotiation: Negotiation
) -> None:
    negotiation.accept_offer(party=offeree)

    assert negotiation.resolution == Resolution.ACCEPTED


def test_cannot_accept_accepted_negotiation(
    offeree: UUID, negotiation: Negotiation
) -> None:
    negotiation.accept_offer(party=offeree)

    with pytest.raises(NegotiationClosed):
        negotiation.accept_offer(party=offeree)


def test_cannot_accept_negotiation_as_offerer(
    owner: UUID, offerer: UUID, negotiation: Negotiation
) -> None:
    with pytest.raises(WaitingForOtherSide):
        negotiation.accept_offer(party=offerer)


def test_cannot_accept_rejected_negotiation(
    offeree: UUID, negotiation: Negotiation
) -> None:
    negotiation.reject_offer(party=offeree)

    with pytest.raises(NegotiationClosed):
        negotiation.accept_offer(party=offeree)


def test_rejected_negotiation_has_rejected_resolution(
    owner: UUID, negotiation: Negotiation
) -> None:
    negotiation.reject_offer(party=owner)

    assert negotiation.resolution == Resolution.REJECTED


def test_cannot_reject_rejected_negotiation(
    owner: UUID, negotiation: Negotiation
) -> None:
    negotiation.reject_offer(party=owner)

    with pytest.raises(NegotiationClosed):
        negotiation.reject_offer(party=owner)


def test_can_reject_negotiation_as_offerer(
    owner: UUID, offerer: UUID, negotiation: Negotiation
) -> None:
    negotiation.reject_offer(party=offerer)

    assert negotiation.resolution == Resolution.REJECTED


def test_cannot_reject_accepted_negotiation(
    offeree: UUID, offerer: UUID, negotiation: Negotiation
) -> None:
    negotiation.accept_offer(party=offeree)

    with pytest.raises(NegotiationClosed):
        negotiation.reject_offer(party=offeree)


def test_cannot_counter_offer_on_accepted_negotiation(
    offeree: UUID, offerer: UUID, negotiation: Negotiation
) -> None:
    negotiation.accept_offer(party=offeree)

    with pytest.raises(NegotiationClosed):
        negotiation.propose_counter_offer(
            party=offerer, counter_offer=Money(Currency.from_code("USD"), "2")
        )


def test_cannot_counter_offer_on_rejected_negotiation(
    owner: UUID, offerer: UUID, negotiation: Negotiation
) -> None:
    negotiation.reject_offer(party=owner)

    with pytest.raises(NegotiationClosed):
        negotiation.propose_counter_offer(
            party=offerer, counter_offer=Money(Currency.from_code("USD"), "2")
        )


def test_counter_offer_changes_offer(
    owner: UUID, offerer: UUID, negotiation: Negotiation
) -> None:
    negotiation.propose_counter_offer(
        party=offerer, counter_offer=Money(Currency.from_code("USD"), "13")
    )

    assert negotiation.offer == Money(Currency.from_code("USD"), "13")


def test_offeree_can_accept_counter_offer(
    offeree: UUID, offerer: UUID, negotiation: Negotiation
) -> None:
    negotiation.propose_counter_offer(
        party=offeree, counter_offer=Money(Currency.from_code("USD"), "19.99")
    )

    negotiation.accept_offer(party=offerer)

    assert negotiation.resolution == Resolution.ACCEPTED
