from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.sqlite import JSON

from used_stuff_market.db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer(), primary_key=True)
    search = Column(String(), nullable=False)
    data = Column(JSONB().with_variant(JSON, "sqlite"), nullable=False)
