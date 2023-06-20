from sqlalchemy import Column, Computed, Index, Integer
from sqlalchemy.dialects.postgresql import JSONB

from used_stuff_market.db import Base
from used_stuff_market.db.tsvector import TSVector


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer(), primary_key=True)
    data = Column(JSONB(), nullable=False)

    ts_vector = Column(
        TSVector(),
        Computed(
            (
                "to_tsvector('english', COALESCE(data->>'title', '') || "
                "' ' || COALESCE(data->>'description', ''))"
            ),
            persisted=True,
        ),
    )
    __table_args__ = (
        Index("ix_ts_vector", ts_vector, postgresql_using="gin"),
        {"schema": "catalog"},
    )
