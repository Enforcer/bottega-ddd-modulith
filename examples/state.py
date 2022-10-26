import abc

from used_stuff_market.shared_kernel.money import Money


class AuctionState(abc.ABC):
    @abc.abstractmethod
    def bid(self, new_price: Money) -> None:
        pass

    @abc.abstractmethod
    def close_auction(self) -> None:
        pass


class OngoingAuction(AuctionState):
    pass


class Auction:
    def __init__(self, price: Money) -> None:
        self._price = price
        self._state = OngoingAuction()

    def bid(self, new_price: Money) -> None:
        self._state.bid(...)

    def close_auction(self) -> None:
        new_state = self._state.close_auction(...)
        self._state = new_state

