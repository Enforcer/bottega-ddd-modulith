from enum import Enum
from uuid import UUID

from used_stuff_market.shared_kernel.money import Money


class NegotiationClosed(Exception):
    pass


class WaitingForOtherSide(Exception):
    pass


class OwnerNeedsToParticipate(Exception):
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
        if owner not in (offeree, offerer):
            raise OwnerNeedsToParticipate

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
    def owner(self) -> UUID:
        return self._owner

    @property
    def offerer(self) -> UUID:
        return self._offerer

    @property
    def offeree(self) -> UUID:
        return self._offeree

    @property
    def offer(self) -> Money:
        return self._offer

    @property
    def resolution(self) -> Resolution | None:
        return self._resolution

    def accept_offer(self, party: UUID) -> None:
        if self._who_offers == party:
            raise WaitingForOtherSide
        if self._resolution is not None:
            raise NegotiationClosed
        self._resolution = Resolution.ACCEPTED

    def reject_offer(self, party: UUID) -> None:
        if self._resolution is not None:
            raise NegotiationClosed
        self._resolution = Resolution.REJECTED

    def propose_counter_offer(self, party: UUID, counter_offer: Money) -> None:
        if self._resolution is not None:
            raise NegotiationClosed

        if party == self._offerer:
            self._who_offers = self._offerer
        else:
            self._who_offers = self._offeree

        self._offer = counter_offer
