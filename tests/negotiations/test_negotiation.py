from typing import Any
from uuid import uuid4

import factory
import pytest

from used_stuff_market.negotiations.negotiation import (
    Negotiation,
    NegotiationClosed,
    Resolution,
    WaitingForOtherSide,
)
from used_stuff_market.shared_kernel.money import Currency, Money


class NegotiationFactory(factory.Factory):
    class Meta:
        model = Negotiation

    class Params:
        who_is_owner = "offeree"

    item_id = factory.Sequence(lambda n: n)
    offer = Money(Currency.from_code("USD"), "9.99")
    offerer = factory.LazyFunction(uuid4)
    offeree = factory.LazyFunction(uuid4)
    owner = factory.LazyAttribute(
        lambda o: o.offeree if o.who_is_owner == "offeree" else o.offerer
    )


class AcceptedNegotiation(NegotiationFactory):
    resolution = Resolution.ACCEPTED


class RejectedNegotiation(NegotiationFactory):
    resolution = Resolution.REJECTED


@pytest.fixture(params=["offeree", "offerer"])
def negotiation(request) -> Negotiation:
    return NegotiationFactory(who_is_owner=request.param)


@pytest.fixture(params=["offeree", "offerer"])
def accepted_negotiation(request) -> Negotiation:
    return AcceptedNegotiation(who_is_owner=request.param)


@pytest.fixture(params=["offeree", "offerer"])
def rejected_negotiation(request) -> Negotiation:
    return RejectedNegotiation(who_is_owner=request.param)


def test_accepted_negotiation_has_accepted_resolution(
    accepted_negotiation: Negotiation,
) -> None:
    assert accepted_negotiation.resolution == Resolution.ACCEPTED


def test_cannot_accept_accepted_negotiation(accepted_negotiation: Negotiation) -> None:
    with pytest.raises(NegotiationClosed):
        accepted_negotiation.accept_offer(party=accepted_negotiation.offeree)


def test_cannot_accept_negotiation_as_offerer(negotiation: Negotiation) -> None:
    with pytest.raises(WaitingForOtherSide):
        negotiation.accept_offer(party=negotiation.offerer)


def test_cannot_accept_rejected_negotiation(rejected_negotiation: Negotiation) -> None:
    with pytest.raises(NegotiationClosed):
        rejected_negotiation.accept_offer(party=rejected_negotiation.offeree)


def test_rejected_negotiation_has_rejected_resolution(
    rejected_negotiation: Negotiation,
) -> None:
    assert rejected_negotiation.resolution == Resolution.REJECTED


def test_cannot_reject_rejected_negotiation(rejected_negotiation: Negotiation) -> None:
    with pytest.raises(NegotiationClosed):
        rejected_negotiation.reject_offer(party=rejected_negotiation.offeree)


def test_can_reject_negotiation_as_offerer(negotiation: Negotiation) -> None:
    negotiation.reject_offer(party=negotiation.offerer)

    assert negotiation.resolution == Resolution.REJECTED


def test_cannot_reject_accepted_negotiation(accepted_negotiation: Negotiation) -> None:
    with pytest.raises(NegotiationClosed):
        accepted_negotiation.reject_offer(party=accepted_negotiation.offeree)


def test_cannot_counter_offer_on_accepted_negotiation(
    accepted_negotiation: Negotiation,
) -> None:
    with pytest.raises(NegotiationClosed):
        accepted_negotiation.propose_counter_offer(
            party=accepted_negotiation.offerer,
            counter_offer=Money(Currency.from_code("USD"), "2"),
        )


def test_cannot_counter_offer_on_rejected_negotiation(
    rejected_negotiation: Negotiation,
) -> None:
    with pytest.raises(NegotiationClosed):
        rejected_negotiation.propose_counter_offer(
            party=rejected_negotiation.offerer,
            counter_offer=Money(Currency.from_code("USD"), "2"),
        )


def test_counter_offer_changes_offer(negotiation: Negotiation) -> None:
    negotiation.propose_counter_offer(
        party=negotiation.offerer,
        counter_offer=Money(Currency.from_code("USD"), "13"),
    )

    assert negotiation.offer == Money(Currency.from_code("USD"), "13")


def test_offeree_can_accept_counter_offer(negotiation: Negotiation) -> None:
    negotiation.propose_counter_offer(
        party=negotiation.offeree,
        counter_offer=Money(Currency.from_code("USD"), "19.99"),
    )

    negotiation.accept_offer(party=negotiation.offerer)

    assert negotiation.resolution == Resolution.ACCEPTED
