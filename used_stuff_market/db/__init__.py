from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    registry,
    sessionmaker,
)

from used_stuff_market.db.settings import DbSettings

engine = create_engine(str(DbSettings().URL), future=True, echo=True)
session_factory = sessionmaker(bind=engine)


metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata


mapper_registry = registry(metadata=metadata)
