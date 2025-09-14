from dataclasses import dataclass
from datetime import timedelta, datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from used_stuff_market.availability import Availability
from used_stuff_market.items import Items
from used_stuff_market.orders.address import Address
from used_stuff_market.orders.calculator import calculate_cost
from used_stuff_market.orders.delivery_method import DeliveryMethod
from used_stuff_market.orders.order import Order
from used_stuff_market.payments import Payments

__all__ = ["Orders", "DeliveryMethod", "Address", "OrderDto"]

from used_stuff_market.shared_kernel.money import Money


@dataclass(frozen=True)
class OrderDto:
    id: int
    address: Address
    item_price: Money
    total: Money
    shipping_cost: Money
    paid_at: datetime | None
    shipped_at: datetime | None


class Orders:
    def __init__(
        self,
        session: Session,
        items: Items,
        availability: Availability,
        payments: Payments,
    ) -> None:
        self._session = session
        self._items = items
        self._availability = availability
        self._payments = payments

    def place(
        self,
        owner_id: UUID,
        item_id: int,
        delivery_method: DeliveryMethod,
        address: Address,
    ) -> None:
        self._availability.lock(
            resource_id=item_id, lock_for=owner_id, duration=timedelta(days=2)
        )

        item_price = self._items.get_item_price(item_id)
        total = calculate_cost(item_price, delivery_method)

        order = Order(
            owner_id=owner_id,
            item_price=item_price,
            total=total,
            address=address,
            paid_at=None,
            shipped_at=None,
        )
        self._session.add(order)
        self._session.flush()

        self._payments.initialize(
            owner_id=owner_id,
            uuid=uuid4(),
            amount=total,
            description=f"Payment for order #{order.id}",
        )

    def get_pending_orders(self, owner_id: UUID) -> list[OrderDto]:
        stmt = select(Order).where(Order.owner_id == owner_id)
        orders = self._session.execute(stmt).scalars().all()
        return [
            OrderDto(
                id=order.id,
                address=order.address,
                item_price=order.item_price,
                total=order.total,
                shipping_cost=order.shipping_cost,
                paid_at=order.paid_at,
                shipped_at=order.shipped_at,
            )
            for order in orders
        ]
