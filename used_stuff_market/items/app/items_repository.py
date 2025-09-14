import abc
from typing import Sequence
from uuid import UUID

from used_stuff_market.items.domain.item import Item


class ItemsRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item: Item) -> None:
        pass

    @abc.abstractmethod
    def get(self, item_id: int) -> Item:
        pass

    @abc.abstractmethod
    def for_owner(self, owner_id: UUID) -> Sequence[Item]:
        pass
