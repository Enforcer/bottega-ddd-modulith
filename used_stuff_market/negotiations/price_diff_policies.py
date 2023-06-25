from abc import ABC, abstractmethod
from decimal import Decimal


class PriceDiffPolicy(ABC):
    @abstractmethod
    def validate(self, old_price: Decimal, new_price: Decimal) -> None:
        pass


class NoLimits(PriceDiffPolicy):
    def validate(self, old_price: Decimal, new_price: Decimal) -> None:
        return None


class NoMoreThan10USD(PriceDiffPolicy):
    def validate(self, old_price: Decimal, new_price: Decimal) -> None:
        if abs(new_price - old_price) > Decimal("10"):
            raise ValueError("Price can't be counter-offered by more than 10 USD")


class NoMoreThan30Percent(PriceDiffPolicy):
    def validate(self, old_price: Decimal, new_price: Decimal) -> None:
        difference = abs(new_price - old_price)
        if difference > old_price * Decimal("0.3"):
            raise ValueError("Price can't be counter-offered by more than 30%")
