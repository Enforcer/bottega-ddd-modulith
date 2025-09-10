import inspect
import enum
from collections import defaultdict
from decimal import Decimal, DecimalException
from functools import total_ordering
from typing import Any, Callable, ClassVar, Tuple, Type


class EventBus:
    def __init__(self) -> None:
        self._subscriptions: dict[Type[Any], list[Callable[[Any], None]]] = defaultdict(
            list
        )

    def subscribe(self, event: Type[Any], subscriber: Callable[[Any], None]) -> None:
        self._subscriptions[event].append(subscriber)

    def publish(self, event: Any) -> None:
        for subscriber in self._subscriptions[type(event)]:
            subscriber(event)


event_bus = EventBus()


class Currency:
    decimal_precision: ClassVar[int]
    iso_code: ClassVar[str]
    __subclasses: ClassVar[dict[str, Type["Currency"]]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        cls.__subclasses[cls.__name__] = cls

    @classmethod
    def from_code(cls, name: str) -> Type["Currency"]:
        try:
            return cls.__subclasses[name]
        except KeyError:
            raise ValueError(f"Invalid currency '{name}'!")


class USD(Currency):
    decimal_precision = 2
    iso_code = "USD"


class EUR(Currency):
    decimal_precision = 2
    iso_code = "EUR"


def validate_amount(currency: Type[Currency], amount: Decimal) -> Decimal:
    try:
        decimal_amount = Decimal(amount).normalize()
    except DecimalException:
        raise ValueError(f'"{amount}" is not a valid amount!')
    else:
        decimal_tuple = decimal_amount.as_tuple()
        if decimal_tuple.sign:
            raise ValueError("amount must not be negative!")
        elif not isinstance(decimal_tuple.exponent, int):
            raise ValueError("unexpected exponent")
        elif -decimal_tuple.exponent > currency.decimal_precision:
            raise ValueError(
                f"given amount has invalid precision! It should have "
                f"no more than {currency.decimal_precision} decimal places!"
            )

    return decimal_amount


@total_ordering
class Money:
    def __init__(self, currency: Type[Currency], amount: Any) -> None:
        if not inspect.isclass(currency) or not issubclass(currency, Currency):
            raise ValueError(f"{currency} is not a subclass of Currency!")

        decimal_amount = validate_amount(currency, amount)

        self._currency = currency
        self._amount = decimal_amount

    @property
    def currency(self) -> Type[Currency]:
        return self._currency

    @property
    def amount(self) -> Decimal:
        return self._amount

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Money):
            raise TypeError
        return self.currency == other.currency and self.amount == other.amount

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Money):
            raise TypeError(
                f"'<' not supported between instances "
                f"of 'Money' and '{other.__class__.__name__}'"
            )
        elif self.currency != other.currency:
            raise TypeError("Can not compare money in different currencies!")
        else:
            return self.amount < other.amount

    def __mul__(self, other: Any) -> "Money":
        assert isinstance(other, int)
        return Money(self.currency, self.amount * other)

    def __add__(self, other: Any) -> "Money":
        assert isinstance(other, Money)
        assert self.currency == other.currency
        return Money(self.currency, self.amount + other.amount)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.currency.__name__}, '{self.amount}')>"

    def __composite_values__(self) -> Tuple[str, Decimal]:
        return self.currency.__name__, self.amount


class DeliveryMethod(enum.Enum):
    COURIER = "COURIER"
    POSTAL_SERVICE = "POSTAL_SERVICE"
    PARCEL_LOCKER = "PARCEL_LOCKER"


DELIVERY_METHOD_TO_FEE: dict[DeliveryMethod, Decimal] = {
    DeliveryMethod.COURIER: Decimal("20"),
    DeliveryMethod.PARCEL_LOCKER: Decimal("8.99"),
    DeliveryMethod.POSTAL_SERVICE: Decimal("15.00"),
}


def calculate_cost(item_price: Money, delivery_method: DeliveryMethod) -> Money:
    new_amount = round((item_price.amount * Decimal("1.05")) + Decimal("2.9"), 2)
    item_price_with_provision = Money(item_price.currency, new_amount)
    delivery_method_fee = Money(
        item_price.currency, DELIVERY_METHOD_TO_FEE[delivery_method]
    )
    total = item_price_with_provision + delivery_method_fee
    return total
