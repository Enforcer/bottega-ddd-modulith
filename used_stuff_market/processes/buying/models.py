from sqlalchemy import Column, DateTime, Integer, Numeric, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import composite

from used_stuff_market.db import mapper_registry, metadata
from used_stuff_market.processes.buying.state import BuyingProcessState
from used_stuff_market.shared_kernel.money import Currency, Money

buying_process_state_table = Table(
    "buying",
    metadata,
    Column("item_id", Integer(), primary_key=True),
    Column("payment_id", UUID(as_uuid=True)),
    Column("buyer_id", UUID(as_uuid=True)),
    Column("price_amount", Numeric()),
    Column("currency", String(3)),
    Column("payment_timeout_at", DateTime()),
    Column("payment_finished_at", DateTime()),
    Column("result", String(128)),
    schema="processes",
)


mapper_registry.map_imperatively(
    BuyingProcessState,
    buying_process_state_table,
    properties={
        "price": composite(
            lambda currency_code, amount: Money(
                Currency.from_code(currency_code), amount
            ),
            buying_process_state_table.c.currency,
            buying_process_state_table.c.price_amount,
        ),
    },
)
