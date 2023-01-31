from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID

from used_stuff_market.db import Base, guid


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer(), primary_key=True)
    owner_id = Column(UUID().with_variant(guid.GUID, "sqlite"), nullable=False)
    created_at = Column(DateTime(), nullable=False)
    locked_by = Column(UUID().with_variant(guid.GUID, "sqlite"), nullable=True)
    locked_to = Column(DateTime(), nullable=True)
