from sqlalchemy import Column, Integer

from used_stuff_market.db import Base


class Placeholder(Base):
    """Replace me with something that actually has any meaning."""

    __tablename__ = "placeholder"
    __table_args__ = {"schema": "processes"}

    id = Column(Integer(), primary_key=True)
