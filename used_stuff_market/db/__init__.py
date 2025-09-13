from contextlib import contextmanager
from typing import Any, Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SessionCls
from sqlalchemy.orm import as_declarative, registry, sessionmaker

from used_stuff_market.db.settings import DbSettings

engine = create_engine(str(DbSettings().URL), future=True, echo=True)
session_factory = sessionmaker(bind=engine)


@as_declarative()
class Base:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass


metadata = Base.metadata  # type: ignore
mapper_registry = registry(metadata=metadata)


@contextmanager
def db_session() -> Iterator[SessionCls]:
    session = session_factory()
    try:
        yield session
    except Exception:
        raise
    finally:
        session.close()
