from datetime import timedelta
from decimal import Decimal
from uuid import UUID, uuid4

from used_stuff_market.availability import Availability
from used_stuff_market.orders import calculator
from used_stuff_market.orders.delivery_method import DeliveryMethod
from used_stuff_market.payments import Payments
from used_stuff_market.shared_kernel.money import Currency, Money


class Orders:
    def order(
        self, buyer_id: UUID, item_id: int, delivery_method: DeliveryMethod
    ) -> None:
        availability = Availability()
        availability.lock(
            resource_id=item_id, lock_for=buyer_id, duration=timedelta(days=2)
        )

        item_price = Money(Currency.from_code("USD"), Decimal("10"))  # TODO
        cost = calculator.calculate_cost(
            item_price=item_price, delivery_method=delivery_method
        )
        payments = Payments()
        payments.initialize(
            owner_id=buyer_id, uuid=uuid4(), amount=cost, description=""
        )
