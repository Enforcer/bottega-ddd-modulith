from decimal import Decimal

from used_stuff_market.orders.delivery_method import DeliveryMethod
from used_stuff_market.shared_kernel.money import Money

DELIVERY_METHOD_TO_FEE: dict[DeliveryMethod, Money] = {
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
