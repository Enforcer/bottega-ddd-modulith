import factory
from pydantic.errors import Decimal

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
