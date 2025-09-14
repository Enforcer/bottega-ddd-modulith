from datetime import datetime
from uuid import UUID

from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, composite
from used_stuff_market.db import Base
from used_stuff_market.orders.address import Address
from used_stuff_market.shared_kernel.money import Money


class Order(Base):
    __tablename__ = "orders"

    id: int
    owner_id: UUID
    item_price: Money
    total: Money
    address: Address
    paid_at: datetime | None
    shipped_at: datetime | None

    @property
    def shipping_cost(self) -> Money:
        return self.total - self.item_price
