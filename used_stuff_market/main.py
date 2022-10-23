from lagom import Container

from used_stuff_market.items import ItemsRepository
from used_stuff_market.items_infrastructure.repository import SqlAlchemyItemsRepository

container = Container()

container[ItemsRepository] = SqlAlchemyItemsRepository  # type: ignore
