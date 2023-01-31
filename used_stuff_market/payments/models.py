from sqlalchemy import Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from used_stuff_market.db import Base, guid


class Payment(Base):
    __tablename__ = "payments"

    uuid = Column(
        UUID(as_uuid=True).with_variant(guid.GUID, "sqlite"), primary_key=True
    )
    owner_id = Column(
        UUID(as_uuid=True).with_variant(guid.GUID, "sqlite"), nullable=False
    )
    created_at = Column(DateTime(), nullable=False)
    amount = Column(Numeric(), nullable=False)
    currency = Column(String(3), nullable=False)
    description = Column(String(), nullable=False)
    status = Column(String(), nullable=False, default="PENDING")

    def mark_as_finished(self) -> None:
        self.status = "FINISHED"
