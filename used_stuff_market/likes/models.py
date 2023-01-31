from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID

from used_stuff_market.db import Base, guid


class Like(Base):
    __tablename__ = "likes"

    item_id = Column(Integer(), primary_key=True)
    liker = Column(
        UUID(as_uuid=True).with_variant(guid.GUID, "sqlite"), primary_key=True
    )
