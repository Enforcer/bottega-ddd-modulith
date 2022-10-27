from uuid import UUID

from used_stuff_market.negotiations.strategies import (
    NegotiationStrategy,
    NoRestrictions,
)
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
        offer: Money,
        offerer: UUID,
        offeree: UUID,
        price_verification_strategy: NegotiationStrategy = NoRestrictions(),
    ) -> None:
        """
        :param offer: how much was originally offered?
        :param oferrer: who offered that price?
        :param oferee: who is this price offered to?
        """
        self._offer = offer
        self._offerer = offerer
        self._offeree = offeree
        self._ended = False
        self._who_offers = offerer
        self._price_verification = price_verification_strategy

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
        self._price_verification.validate_offer(
            current_offer=self._offer, new_offer=counter_offer
        )
        if self._ended:
            raise NegotiationClosed
        if self._who_offers == party:
            raise CannotCounterOwnOffer

        self._who_offers = party
        self._offer = counter_offer
