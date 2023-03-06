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


class OfferFactory(factory.Factory):
    class Meta:
        model = Money

    amount = "9.99"
    currency = Currency.from_code("USD")


class NegotiationFactory(factory.Factory):
    class Meta:
        model = Negotiation

    item_id = factory.Sequence(lambda n: n)
    offer = factory.SubFactory(OfferFactory)
    offerer = factory.LazyFunction(uuid4)
    offeree = factory.LazyFunction(uuid4)
    owner = factory.LazyAttribute(lambda o: o.offeree)


class AcceptedNegotiation(NegotiationFactory):
    resolution = Resolution.ACCEPTED


class AlternativeAcceptedNegotiation(NegotiationFactory):
    @factory.post_generation
    def accept(obj: Negotiation, create: bool, extracted: Any, **kwargs: Any) -> None:
        obj.accept_offer(party=obj.offeree)


@pytest.fixture()
def negotiation() -> Negotiation:
    return NegotiationFactory()


def test_accepted_negotiation_has_accepted_resolution() -> None:
    negotiation = AcceptedNegotiation()

    assert negotiation.resolution == Resolution.ACCEPTED


def test_cannot_accept_accepted_negotiation() -> None:
    negotiation = AlternativeAcceptedNegotiation()

    with pytest.raises(NegotiationClosed):
        negotiation.accept_offer(party=negotiation.offeree)


def test_cannot_accept_negotiation_as_offerer(
    negotiation: Negotiation
) -> None:
    with pytest.raises(WaitingForOtherSide):
        negotiation.accept_offer(party=negotiation.offerer)


def test_cannot_accept_rejected_negotiation(
    negotiation: Negotiation
) -> None:
    negotiation.reject_offer(party=negotiation.offeree)

    with pytest.raises(NegotiationClosed):
        negotiation.accept_offer(party=negotiation.offeree)


def test_rejected_negotiation_has_rejected_resolution(
    negotiation: Negotiation
) -> None:
    negotiation.reject_offer(party=negotiation.offeree)

    assert negotiation.resolution == Resolution.REJECTED


def test_cannot_reject_rejected_negotiation(
    negotiation: Negotiation
) -> None:
    negotiation.reject_offer(party=negotiation.offeree)

    with pytest.raises(NegotiationClosed):
        negotiation.reject_offer(party=negotiation.offeree)


def test_can_reject_negotiation_as_offerer(
    negotiation: Negotiation
) -> None:
    negotiation.reject_offer(party=negotiation.offerer)

    assert negotiation.resolution == Resolution.REJECTED


def test_cannot_reject_accepted_negotiation(
    negotiation: Negotiation
) -> None:
    negotiation.accept_offer(party=negotiation.offeree)

    with pytest.raises(NegotiationClosed):
        negotiation.reject_offer(party=negotiation.offeree)


def test_cannot_counter_offer_on_accepted_negotiation(
    negotiation: Negotiation
) -> None:
    negotiation.accept_offer(party=negotiation.offeree)

    with pytest.raises(NegotiationClosed):
        negotiation.propose_counter_offer(
            party=negotiation.offerer,
            counter_offer=Money(Currency.from_code("USD"), "2"),
        )


def test_cannot_counter_offer_on_rejected_negotiation(
    negotiation: Negotiation
) -> None:
    negotiation.reject_offer(party=negotiation.owner)

    with pytest.raises(NegotiationClosed):
        negotiation.propose_counter_offer(
            party=negotiation.offerer,
            counter_offer=Money(Currency.from_code("USD"), "2"),
        )


def test_counter_offer_changes_offer(
    negotiation: Negotiation
) -> None:
    negotiation.propose_counter_offer(
        party=negotiation.offerer,
        counter_offer=Money(Currency.from_code("USD"), "13"),
    )

    assert negotiation.offer == Money(Currency.from_code("USD"), "13")


def test_offeree_can_accept_counter_offer(
    negotiation: Negotiation
) -> None:
    negotiation.propose_counter_offer(
        party=negotiation.offeree,
        counter_offer=Money(Currency.from_code("USD"), "19.99"),
    )

    negotiation.accept_offer(party=negotiation.offerer)

    assert negotiation.resolution == Resolution.ACCEPTED
