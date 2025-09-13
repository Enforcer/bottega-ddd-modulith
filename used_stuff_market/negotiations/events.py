from attr import define

from used_stuff_market.shared_kernel.money import Money


@define(frozen=True)
class PriceAgreed:
    item_id: int
    price: Money
