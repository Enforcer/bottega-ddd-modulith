from lagom import Container
from sqlalchemy.orm import Session

from used_stuff_market.db import ScopedSession
from used_stuff_market.items import ItemsRepository
from used_stuff_market.items_infrastructure.repository import SqlAlchemyItemsRepository

container = Container()

container[ItemsRepository] = SqlAlchemyItemsRepository  # type: ignore
container[Session] = lambda _: ScopedSession()
