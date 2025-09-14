from datetime import datetime
from uuid import UUID

from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, composite
from used_stuff_market.db import Base
from used_stuff_market.orders.address import Address
from used_stuff_market.shared_kernel.money import Money


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[UUID]
    item_price: Mapped[Money] = composite(
        mapped_column("item_price_currency", String(3)),
        mapped_column("item_price_amount", Numeric()),
    )
    total: Mapped[Money] = composite(
        mapped_column("total_currency", String(3)),
        mapped_column("total_amount", Numeric()),
    )
    address: Mapped[Address] = composite(
        mapped_column("line_1"),
        mapped_column("line_2"),
        mapped_column("postal_code"),
        mapped_column("city"),
        mapped_column("country_code"),
    )
    paid_at: Mapped[datetime | None]
    shipped_at: Mapped[datetime | None]

    @property
    def shipping_cost(self) -> Money:
        return self.total - self.item_price
