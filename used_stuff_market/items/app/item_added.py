from dataclasses import dataclass

from used_stuff_market.shared_kernel.money import Money


@dataclass(frozen=True)
class ItemAdded:
    id: int
    title: str
    description: str
    starting_price: Money
