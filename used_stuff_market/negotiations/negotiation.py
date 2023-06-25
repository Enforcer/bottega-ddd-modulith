from decimal import Decimal
from enum import StrEnum

from attr import define


class State(StrEnum):
    WAITING_FOR_SELLER = "waiting_for_seller"
    WAITING_FOR_BUYER = "waiting_for_buyer"
    BROKEN_OFF = "broken_off"
    ACCEPTED = "accepted"

    @property
    def concluded(self) -> bool:
        return self in (State.BROKEN_OFF, State.ACCEPTED)


@define
class Negotiation:
    _item_id: int
    _seller_id: int
    _buyer_id: int
    _state: State
    _price: Decimal
    _currency: str

    class NegotiationConcluded(Exception):
        pass

    class NotAParticipant(Exception):
        pass

    class WaitingForOtherParticipant(Exception):
        pass

    @property
    def price(self) -> Decimal:
        return self._price

    def accept(self, user_id: int) -> None:
        self._validate_participant(user_id)
        self._validate_side(user_id)
        self._validate_not_concluded()

        self._state = State.ACCEPTED

    def break_off(self, user_id: int) -> None:
        self._validate_participant(user_id)
        self._validate_not_concluded()

        self._state = State.BROKEN_OFF

    def counteroffer(self, user_id: int, price: Decimal, currency: str) -> None:
        self._validate_participant(user_id)

        self._price = price
        self._currency = currency
        if user_id == self._seller_id:
            self._state = State.WAITING_FOR_BUYER
        else:
            self._state = State.WAITING_FOR_SELLER

    def _validate_participant(self, user_id: int) -> None:
        if user_id not in (self._seller_id, self._buyer_id):
            raise self.NotAParticipant

    def _validate_not_concluded(self) -> None:
        if self._state.concluded:
            raise self.NegotiationConcluded

    def _validate_side(self, user_id: int) -> None:
        if self._state == State.WAITING_FOR_SELLER and user_id != self._seller_id:
            raise self.WaitingForOtherParticipant
        elif self._state == State.WAITING_FOR_BUYER and user_id != self._buyer_id:
            raise self.WaitingForOtherParticipant
