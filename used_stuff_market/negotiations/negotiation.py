from uuid import UUID

from used_stuff_market.shared_kernel.money import Money


class NegotiationClosed(Exception):
    pass


class CannotAcceptOwnOffer(Exception):
    pass


class CannotRejectOwnOffer(Exception):
    pass


class Negotiation:
    def __init__(self, offer: Money, offerer: UUID, offeree: UUID) -> None:
        """
        :param offer: how much was originally offered?
        :param oferrer: who offered that price?
        :param oferee: who is this price offered to?
        """
        self._offer = offer
        self._offerer = offerer
        self._offeree = offeree
        self._ended = False

    @property
    def offer(self) -> Money:
        return self._offer

    def accept_offer(self, party: UUID) -> None:
        if self._ended:
            raise NegotiationClosed
        if party != self._offeree:
            raise CannotAcceptOwnOffer
        self._ended = True

    def reject_offer(self, party: UUID) -> None:
        if self._ended:
            raise NegotiationClosed
        if party != self._offeree:
            raise CannotRejectOwnOffer
        self._ended = True

    def propose_counter_offer(self, party: UUID, counter_offer: Money) -> None:
        pass
