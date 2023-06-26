from contextlib import contextmanager
from typing import Any

import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SessionCls
from sqlalchemy.orm import as_declarative, registry, scoped_session, sessionmaker

from used_stuff_market.db.settings import DbSettings

engine = create_engine(DbSettings().URL, future=True, echo=True)
session_factory = sessionmaker(bind=engine)
ScopedSession = scoped_session(session_factory)


mongo_client = MongoClient(DbSettings().MONGO_URL)
mongo_db: Database = mongo_client[DbSettings().MONGO_DB]


def migrate_mongo_db() -> None:
    mongo_db["negotiations"].create_index(
        [
            ("item_id", pymongo.ASCENDING),
            ("buyer_id", pymongo.ASCENDING),
            ("seller_id", pymongo.ASCENDING),
        ],
        unique=True,
    )


@as_declarative()
class Base:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass


metadata = Base.metadata  # type: ignore
mapper_registry = registry(metadata=metadata)


@contextmanager
def db_session() -> SessionCls:
    session = ScopedSession()
    try:
        yield session
    except Exception:
        raise
    finally:
        ScopedSession.remove()
