import abc
import random
from uuid import UUID

from used_stuff_market.shared_kernel.money import Currency, Money


class NegotiationStrategy(abc.ABC):
    class PriceNotAllowed(Exception):
        pass

    @abc.abstractmethod
    def validate_offer(self, current_offer: Money, new_offer: Money) -> None:
        pass


class NoRestrictions(NegotiationStrategy):
    def validate_offer(self, current_offer: Money, new_offer: Money) -> None:
        pass


class FivePercentLimit(NegotiationStrategy):
    def validate_offer(self, current_offer: Money, new_offer: Money) -> None:
        difference = abs(new_offer.amount - current_offer.amount) / current_offer.amount
        if difference > 0.05:
            raise self.PriceNotAllowed


class FiveDollarsLimit(NegotiationStrategy):
    def validate_offer(self, current_offer: Money, new_offer: Money) -> None:
        max_difference = Money(Currency.from_code("USD"), "5.00")
        if abs(new_offer.amount - current_offer.amount) > max_difference.amount:
            raise self.PriceNotAllowed


def get_strategy_for_party(party: UUID) -> NegotiationStrategy:
    strategies = NegotiationStrategy.__subclasses__()
    random.seed(party.int)
    strategy_cls = random.choice(strategies)
    return strategy_cls()  # type: ignore
