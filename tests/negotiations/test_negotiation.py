from uuid import uuid4

import pytest

from used_stuff_market.negotiations.negotiation import (
    Negotiation,
    NegotiationClosed,
    Resolution,
    WaitingForOtherSide,
)
from used_stuff_market.shared_kernel.money import Currency, Money


def test_accepted_negotiation_has_accepted_resolution() -> None:
    owner = uuid4()
    negotiation = Negotiation(
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=uuid4(),
        offeree=owner,
    )

    negotiation.accept_offer(party=owner)

    assert negotiation.resolution == Resolution.ACCEPTED


def test_cannot_accept_accepted_negotiation() -> None:
    owner = uuid4()
    negotiation = Negotiation(
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=uuid4(),
        offeree=owner,
    )

    negotiation.accept_offer(party=owner)

    with pytest.raises(NegotiationClosed):
        negotiation.accept_offer(party=owner)


def test_cannot_accept_negotiation_as_offerer() -> None:
    owner = uuid4()
    offerer = uuid4()
    negotiation = Negotiation(
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=offerer,
        offeree=owner,
    )

    with pytest.raises(WaitingForOtherSide):
        negotiation.accept_offer(party=offerer)


def test_cannot_accept_rejected_negotiation() -> None:
    owner = uuid4()
    negotiation = Negotiation(
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=uuid4(),
        offeree=owner,
    )

    negotiation.reject_offer(party=owner)

    with pytest.raises(NegotiationClosed):
        negotiation.accept_offer(party=owner)


def test_rejected_negotiation_has_rejected_resolution() -> None:
    owner = uuid4()
    negotiation = Negotiation(
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=uuid4(),
        offeree=owner,
    )

    negotiation.reject_offer(party=owner)

    assert negotiation.resolution == Resolution.REJECTED


def test_cannot_reject_rejected_negotiation() -> None:
    owner = uuid4()
    negotiation = Negotiation(
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=uuid4(),
        offeree=owner,
    )

    negotiation.reject_offer(party=owner)

    with pytest.raises(NegotiationClosed):
        negotiation.reject_offer(party=owner)


def test_can_reject_negotiation_as_offerer() -> None:
    owner = uuid4()
    offerer = uuid4()
    negotiation = Negotiation(
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=offerer,
        offeree=owner,
    )

    negotiation.reject_offer(party=offerer)

    assert negotiation.resolution == Resolution.REJECTED


def test_cannot_reject_accepted_negotiation() -> None:
    owner = uuid4()
    negotiation = Negotiation(
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=uuid4(),
        offeree=owner,
    )

    negotiation.accept_offer(party=owner)

    with pytest.raises(NegotiationClosed):
        negotiation.reject_offer(party=owner)


def test_cannot_counter_offer_on_accepted_negotiation() -> None:
    owner = uuid4()
    offerer = uuid4()
    negotiation = Negotiation(
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=offerer,
        offeree=owner,
    )

    negotiation.accept_offer(party=owner)

    with pytest.raises(NegotiationClosed):
        negotiation.propose_counter_offer(
            party=offerer, counter_offer=Money(Currency.from_code("USD"), "2")
        )


def test_cannot_counter_offer_on_rejected_negotiation() -> None:
    owner = uuid4()
    offerer = uuid4()
    negotiation = Negotiation(
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=offerer,
        offeree=owner,
    )

    negotiation.reject_offer(party=owner)

    with pytest.raises(NegotiationClosed):
        negotiation.propose_counter_offer(
            party=offerer, counter_offer=Money(Currency.from_code("USD"), "2")
        )


def test_counter_offer_changes_offer() -> None:
    owner = uuid4()
    offerer = uuid4()
    negotiation = Negotiation(
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=offerer,
        offeree=owner,
    )

    negotiation.propose_counter_offer(
        party=offerer, counter_offer=Money(Currency.from_code("USD"), "13")
    )

    assert negotiation.offer == Money(Currency.from_code("USD"), "13")


def test_offeree_can_accept_counter_offer() -> None:
    owner = uuid4()
    offerer = uuid4()
    negotiation = Negotiation(
        item_id=1,
        owner=owner,
        offer=Money(Currency.from_code("USD"), "9.99"),
        offerer=offerer,
        offeree=owner,
    )

    negotiation.propose_counter_offer(
        party=owner, counter_offer=Money(Currency.from_code("USD"), "19.99")
    )

    negotiation.accept_offer(party=offerer)

    assert negotiation.resolution == Resolution.ACCEPTED
