from typing import Sequence
from uuid import UUID

from sqlalchemy import Column, Integer, Numeric, String, Table, select
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import composite

from used_stuff_market.db import ScopedSession, mapper_registry, metadata
from used_stuff_market.items.item import Item
from used_stuff_market.utils import Currency, Money


class ItemsRepository:
    def add(self, item: Item) -> None:
        session = ScopedSession()
        session.add(item)
        session.flush()

    def for_owner(self, owner_id: UUID) -> Sequence[Item]:
        session = ScopedSession()
        stmt = select(Item).where(items.c.owner_id == str(owner_id))
        return session.execute(stmt).scalars().all()


items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("owner_id", PostgresUUID(as_uuid=True)),
    Column("title", String()),
    Column("description", String()),
    Column("starting_price_amount", Numeric()),
    Column("starting_price_currency", String(3)),
    schema="items",
)


mapper_registry.map_imperatively(
    Item,
    items,
    properties={
        "starting_price": composite(
            lambda currency_code, amount: Money(
                Currency.from_code(currency_code), amount
            ),
            items.c.starting_price_currency,
            items.c.starting_price_amount,
        ),
    },
)
