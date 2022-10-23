import abc
from uuid import UUID


from used_stuff_market.items.item import Item


class ItemsRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item: Item) -> None:
        pass

    @abc.abstractmethod
    def for_owner(self, owner_id: UUID) -> list[Item]:
        pass
