from typing import TypedDict
from uuid import UUID

from used_stuff_market.availability import Availability
from used_stuff_market.foundation.event_bus import EventBus
from used_stuff_market.items.app.item_added import ItemAdded
from used_stuff_market.items.domain.item import Item
from used_stuff_market.items.app.items_repository import ItemsRepository
from used_stuff_market.shared_kernel.money import Money


class MoneyDto(TypedDict):
    amount: str
    currency: str


class ItemDto(TypedDict):
    id: int
    title: str
    description: str
    starting_price: MoneyDto


class Items:
    def __init__(
        self,
        repository: ItemsRepository,
        availability: Availability,
        event_bus: EventBus,
    ) -> None:
        self._repository = repository
        self._availability = availability
        self._event_bus = event_bus

    def add(
        self, owner_id: UUID, title: str, description: str, starting_price: Money
    ) -> None:
        item = Item(
            owner_id=owner_id,
            title=title,
            description=description,
            starting_price=starting_price,
        )
        self._repository.add(item)

        item_added = ItemAdded(
            id=item.id,
            title=title,
            description=description,
            starting_price=starting_price,
        )
        self._event_bus.publish(item_added)
        self._availability.register(owner_id=owner_id, resource_id=item.id)

    def get_items(self, owner_id: UUID) -> list[ItemDto]:
        items = self._repository.for_owner(owner_id=owner_id)
        return [
            ItemDto(
                id=item.id,
                title=item.title,
                description=item.description,
                starting_price=MoneyDto(
                    amount=self._format_amount(item.starting_price),
                    currency=item.starting_price.currency.iso_code,
                ),
            )
            for item in items
        ]

    def get_item_price(self, item_id: int) -> Money:
        item = self._repository.get(item_id)
        return item.starting_price

    def _format_amount(self, price: Money) -> str:
        decimal_points = price.currency.decimal_precision
        formatter = "{0:." + str(decimal_points) + "f}"
        return formatter.format(price.amount)
