from uuid import UUID

from used_stuff_market.negotiations.negotiation_id import NegotiationId
from used_stuff_market.shared_kernel.money import Money


class NegotiationClosed(Exception):
    pass


class CannotAcceptOwnOffer(Exception):
    pass


class CannotRejectOwnOffer(Exception):
    pass


class CannotCounterOwnOffer(Exception):
    pass


class Negotiation:
    def __init__(
        self,
        item_id: int,
        owner: UUID,
        offer: Money,
        offerer: UUID,
        offeree: UUID,
        ended: bool = False,
    ) -> None:
        """
        :param offer: how much was originally offered?
        :param oferrer: who offered that price?
        :param oferee: who is this price offered to?
        """
        self._item_id = item_id
        self._owner = owner
        self._offer = offer
        self._offerer = offerer
        self._offeree = offeree
        self._ended = ended
        self._who_offers = offerer

    @property
    def id(self) -> NegotiationId:
        return NegotiationId(
            item_id=self._item_id, offerer=self._offerer, offeree=self._offeree
        )

    @property
    def buyer(self) -> UUID:
        if self._offerer == self._owner:
            return self._offeree
        else:
            return self._offerer

    @property
    def offer(self) -> Money:
        return self._offer

    def accept_offer(self, party: UUID) -> None:
        if self._ended:
            raise NegotiationClosed
        if party == self._who_offers:
            raise CannotAcceptOwnOffer
        self._ended = True

    def reject_offer(self, party: UUID) -> None:
        if self._ended:
            raise NegotiationClosed
        if party == self._who_offers:
            raise CannotRejectOwnOffer
        self._ended = True

    def propose_counter_offer(self, party: UUID, counter_offer: Money) -> None:
        if self._ended:
            raise NegotiationClosed
        if self._who_offers == party:
            raise CannotCounterOwnOffer

        self._who_offers = party
        self._offer = counter_offer
