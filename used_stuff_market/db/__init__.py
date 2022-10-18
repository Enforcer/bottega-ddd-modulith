from typing import Type, cast

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SessionCls
from sqlalchemy.orm import as_declarative, registry, scoped_session, sessionmaker

from used_stuff_market.db.settings import DbSettings

engine = create_engine(DbSettings().URL, future=True, echo=True)
session_factory = sessionmaker(bind=engine)
Session = cast(Type[SessionCls], scoped_session(session_factory))


@as_declarative()
class Base:
    pass


metadata = Base.metadata
mapper_registry = registry(metadata=metadata)
