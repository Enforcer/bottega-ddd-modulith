from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from used_stuff_market.items.item import Item
from used_stuff_market.items.repository import ItemsRepository


class SqlAlchemyItemsRepository(ItemsRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, item: Item) -> None:
        self._session.add(item)
        self._session.flush()

    def for_owner(self, owner_id: UUID) -> list[Item]:
        items: list[Item] = (
            self._session.query(Item).filter(Item.owner_id == str(owner_id)).all()
        )
        return items
