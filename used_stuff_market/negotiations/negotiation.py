from enum import Enum
from uuid import UUID

from used_stuff_market.shared_kernel.money import Money


class NegotiationClosed(Exception):
    pass


class Resolution(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class Negotiation:
    def __init__(
        self,
        item_id: int,
        owner: UUID,
        offer: Money,
        offerer: UUID,
        offeree: UUID,
        resolution: Resolution | None = None,
        who_offers: UUID | None = None,
    ) -> None:
        """
        :param item_id: identifier of an item
        :param owner: who owns the item?
        :param offer: how much was originally offered?
        :param offerer: who offered that price?
        :param offeree: who is this price offered to?
        :param resolution: is this negotiation accepted or rejected?
        :param who_offers: who is currently offering?
            2nd side can accept, reject or counteroffer.
        """
        if who_offers is None:
            who_offers = offerer

        self._item_id = item_id
        self._owner = owner
        self._offer = offer
        self._offerer = offerer
        self._offeree = offeree
        self._resolution = resolution
        self._who_offers = who_offers

    @property
    def offer(self) -> Money:
        return self._offer

    @property
    def resolution(self) -> Resolution | None:
        return self._resolution

    def accept_offer(self, party: UUID) -> None:
        pass

    def reject_offer(self, party: UUID) -> None:
        pass

    def propose_counter_offer(self, party: UUID, counter_offer: Money) -> None:
        pass
