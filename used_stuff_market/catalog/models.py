from sqlalchemy import Computed, Index, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column

from used_stuff_market.db import Base
from used_stuff_market.db.tsvector import TSVector


class Product(Base):
    __tablename__ = "products"

    id = mapped_column(Integer(), primary_key=True)
    data = mapped_column(JSONB(), nullable=False)  # type: ignore

    ts_vector = mapped_column(
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
