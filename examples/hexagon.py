import abc
from typing import TypedDict
from uuid import UUID

from used_stuff_market.items import Item
from used_stuff_market.shared_kernel.money import Money


class MoneyDto(TypedDict):
    amount: str
    currency: str


class ItemDto(TypedDict):
    id: int
    title: str
    description: str
    starting_price: MoneyDto


class AddingItemsUseCase(abc.ABC):
    @abc.abstractmethod
    def add(
        self, owner_id: UUID, title: str, description: str, starting_price: Money
    ) -> ItemDto:
        pass


class ItemsRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item: Item) -> None:
        pass


class Items(AddingItemsUseCase):
    def __init__(self, repository: ItemsRepository) -> None:
        self._repository = repository

    def add(
        self, owner_id: UUID, title: str, description: str, starting_price: Money
    ) -> ItemDto:
        item = Item(
            owner_id=owner_id,
            title=title,
            description=description,
            starting_price=starting_price,
        )
        self._repository.add(item)
        return self._item_to_dto(item)
