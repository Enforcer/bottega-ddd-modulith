from decimal import Decimal

from sqlalchemy import Boolean, Column, Integer, Numeric, String

from used_stuff_market.db import Base, guid
from used_stuff_market.shared_kernel.money import Currency, Money


class Negotiation(Base):
    __tablename__ = "negotiations"

    item_id = Column(Integer(), primary_key=True)
    owner_id = Column(guid.GUID, primary_key=True)
    buyer_id = Column(guid.GUID, primary_key=True)
    amount = Column(Numeric(), nullable=False)
    currency = Column(String(3), nullable=False)
    accepted = Column(Boolean, nullable=False, default=False)

    @property
    def offer(self) -> Money:
        return Money(Currency.from_code(self.currency), Decimal(self.amount))
