from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID

from used_stuff_market.db import Base


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = {"schema": "likes"}

    item_id = Column(Integer(), primary_key=True)
    liker = Column(UUID(as_uuid=True), primary_key=True)
