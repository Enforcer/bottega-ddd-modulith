import abc
from typing import Type
from uuid import UUID

from used_stuff_market.shared_kernel.money import Money


class NegotiationClosed(Exception):
    pass


class CannotAcceptOwnOffer(Exception):
    pass


class CannotRejectOwnOffer(Exception):
    pass


class CannotCounterOwnOffer(Exception):
    pass


class State(abc.ABC):
    def __init__(self, offerer: UUID, offeree: UUID) -> None:
        self._offerer = offerer
        self._offeree = offeree

    @abc.abstractmethod
    def accept_offer(self, party: UUID) -> Type["State"]:
        pass

    @abc.abstractmethod
    def reject_offer(self, party: UUID) -> Type["State"]:
        pass

    @abc.abstractmethod
    def propose_counter_offer(self, party: UUID) -> Type["State"]:
        pass


class WaitingForOfferee(State):
    def accept_offer(self, party: UUID) -> Type["State"]:
        if party == self._offerer:
            raise CannotAcceptOwnOffer
        return Closed

    def reject_offer(self, party: UUID) -> Type["State"]:
        if party == self._offerer:
            raise CannotRejectOwnOffer
        return Closed

    def propose_counter_offer(self, party: UUID) -> Type["State"]:
        if party == self._offerer:
            raise CannotCounterOwnOffer
        return WaitingForOfferer


class WaitingForOfferer(State):
    def accept_offer(self, party: UUID) -> Type["State"]:
        if party == self._offeree:
            raise CannotAcceptOwnOffer
        return Closed

    def reject_offer(self, party: UUID) -> Type["State"]:
        if party == self._offeree:
            raise CannotRejectOwnOffer
        return Closed

    def propose_counter_offer(self, party: UUID) -> Type["State"]:
        if party == self._offeree:
            raise CannotCounterOwnOffer
        return WaitingForOfferee


class Closed(State):
    def accept_offer(self, party: UUID) -> Type["State"]:
        raise NegotiationClosed

    def reject_offer(self, party: UUID) -> Type["State"]:
        raise NegotiationClosed

    def propose_counter_offer(self, party: UUID) -> Type["State"]:
        raise NegotiationClosed


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
        self._state: State = WaitingForOfferee(offerer=offerer, offeree=offeree)

    @property
    def offer(self) -> Money:
        return self._offer

    def accept_offer(self, party: UUID) -> None:
        new_state_cls = self._state.accept_offer(party)
        self._state = new_state_cls(offerer=self._offerer, offeree=self._offeree)

    def reject_offer(self, party: UUID) -> None:
        new_state_cls = self._state.reject_offer(party)
        self._state = new_state_cls(offerer=self._offerer, offeree=self._offeree)

    def propose_counter_offer(self, party: UUID, counter_offer: Money) -> None:
        new_state_cls = self._state.propose_counter_offer(party)
        self._state = new_state_cls(offerer=self._offerer, offeree=self._offeree)
        self._offer = counter_offer
