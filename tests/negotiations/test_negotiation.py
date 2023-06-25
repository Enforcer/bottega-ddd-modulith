from decimal import Decimal

import factory
import pytest

from used_stuff_market.negotiations.negotiation import Negotiation, State

ITEM_ID = 1
SELLER_ID = 2
BUYER_ID = 3
OTHER_DUDE = 4


class NegotiationFactory(factory.Factory):
    class Meta:
        model = Negotiation

    item_id = ITEM_ID
    seller_id = SELLER_ID
    buyer_id = BUYER_ID
    state = State.WAITING_FOR_SELLER
    price = Decimal("9.99")
    currency = "USD"


def test_accepted_negotiation_cannot_be_accepted_again() -> None:
    negotiation = NegotiationFactory.build()
    negotiation.accept(user_id=SELLER_ID)

    with pytest.raises(Negotiation.NegotiationConcluded):
        negotiation.accept(user_id=SELLER_ID)


def test_cannot_be_accepted_by_seller_if_they_offered_price() -> None:
    negotiation = NegotiationFactory.build(state=State.WAITING_FOR_BUYER)

    with pytest.raises(Negotiation.WaitingForOtherParticipant):
        negotiation.accept(user_id=SELLER_ID)


def test_accepted_negotiation_cannot_be_broken_off() -> None:
    negotiation = NegotiationFactory.build()
    negotiation.accept(user_id=SELLER_ID)

    with pytest.raises(Negotiation.NegotiationConcluded):
        negotiation.break_off(user_id=SELLER_ID)


def test_cannot_be_accepted_by_someone_other_than_buyer_or_seller() -> None:
    negotiation = NegotiationFactory.build()
    with pytest.raises(Negotiation.NotAParticipant):
        negotiation.accept(user_id=OTHER_DUDE)


def test_cannot_be_broken_off_by_someone_other_than_buyer_or_seller() -> None:
    negotiation = NegotiationFactory.build()
    with pytest.raises(Negotiation.NotAParticipant):
        negotiation.break_off(user_id=OTHER_DUDE)


def test_cannot_be_counter_offered_by_someone_other_than_buyer_or_seller() -> None:
    negotiation = NegotiationFactory.build()
    with pytest.raises(Negotiation.NotAParticipant):
        negotiation.counteroffer(
            user_id=OTHER_DUDE, price=Decimal("12.99"), currency="USD"
        )


def test_counter_offering_changes_price() -> None:
    negotiation = NegotiationFactory.build(price=Decimal("9.99"))
    negotiation.counteroffer(user_id=SELLER_ID, price=Decimal("12.99"), currency="USD")
    assert negotiation.price == Decimal("12.99")
