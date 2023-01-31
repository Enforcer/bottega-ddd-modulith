from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, LargeBinary, String

from used_stuff_market.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(LargeBinary(255), nullable=False)
    created_at = Column(DateTime(), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(), nullable=False, default=datetime.utcnow)
