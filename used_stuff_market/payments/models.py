from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from used_stuff_market.db import Base


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = {"schema": "payments"}

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True)
    owner_id = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at = mapped_column(DateTime(), nullable=False)
    amount = mapped_column(Numeric(), nullable=False)
    currency = mapped_column(String(3), nullable=False)
    description = mapped_column(String(), nullable=False)
    status = mapped_column(String(), nullable=False, default="PENDING")

    def mark_as_finished(self) -> None:
        self.status = "FINISHED"
