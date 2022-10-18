from datetime import timedelta
from uuid import UUID, uuid4

from used_stuff_market.availability import Availability
from used_stuff_market.orders import calculator
from used_stuff_market.orders.delivery_method import DeliveryMethod
from used_stuff_market.payments import Payments


class Orders:
    def order(
        self, buyer_id: UUID, item_id: int, delivery_method: DeliveryMethod
    ) -> None:
        pass
