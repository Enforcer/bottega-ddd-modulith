from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from used_stuff_market.items.app.items_repository import ItemsRepository
from used_stuff_market.items.domain.item import Item
from used_stuff_market.items.infrastructure.items_table import items


class SqlAlchemyItemsRepository(ItemsRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, item: Item) -> None:
        self._session.add(item)
        self._session.flush()

    def get(self, item_id: int) -> Item:
        stmt = select(Item).where(items.c.id == item_id)
        return self._session.execute(stmt).scalars().one()

    def for_owner(self, owner_id: UUID) -> Sequence[Item]:
        stmt = select(Item).where(items.c.owner_id == owner_id)
        return self._session.execute(stmt).scalars().all()
