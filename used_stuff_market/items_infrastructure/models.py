from sqlalchemy import Column, Integer, Numeric, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import composite

from used_stuff_market.db import mapper_registry, metadata
from used_stuff_market.items.item import Item
from used_stuff_market.shared_kernel.money import Currency, Money

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("owner_id", UUID(as_uuid=True)),
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
