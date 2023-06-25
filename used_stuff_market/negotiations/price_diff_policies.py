from abc import ABC, abstractmethod
from decimal import Decimal


class PriceDiffPolicy(ABC):
    @abstractmethod
    def validate(self, old_price: Decimal, new_price: Decimal) -> None:
        pass
