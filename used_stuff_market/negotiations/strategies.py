import abc
import random
from uuid import UUID

from used_stuff_market.shared_kernel.money import Money


class NegotiationStrategy(abc.ABC):
    class PriceNotAllowed(Exception):
        pass

    @abc.abstractmethod
    def validate_offer(self, current_offer: Money, new_offer: Money) -> None:
        pass


def get_strategy_for_party(party: UUID) -> NegotiationStrategy:
    strategies = NegotiationStrategy.__subclasses__()
    random.seed(party.int)
    strategy_cls = random.choice(strategies)
    return strategy_cls()  # type: ignore
