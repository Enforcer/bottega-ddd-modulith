from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, LargeBinary, String
from sqlalchemy.orm import mapped_column

from used_stuff_market.db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "users"}

    id = mapped_column(Integer(), primary_key=True)
    username = mapped_column(String(255), unique=True, nullable=False)
    password = mapped_column(LargeBinary(255), nullable=False)
    created_at = mapped_column(
        DateTime(), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = mapped_column(
        DateTime(), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
