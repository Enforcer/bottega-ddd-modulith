from typing import TypedDict
from uuid import UUID

from used_stuff_market.availability import Availability
from used_stuff_market.catalog import Catalog
from used_stuff_market.items.item import Item
from used_stuff_market.items.repository import ItemsRepository
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
    def add(
        self, owner_id: UUID, title: str, description: str, starting_price: Money
    ) -> None:
        item = Item(
            owner_id=owner_id,
            title=title,
            description=description,
            starting_price=starting_price,
        )
        repository = ItemsRepository()
        repository.add(item)

        Catalog().add(
            id=item.id,
            data={
                "title": title,
                "description": description,
                "starting_price": {
                    "amount": self._format_amount(item.starting_price),
                    "currency": item.starting_price.currency.iso_code,
                },
            },
        )
        Availability().register(owner_id=owner_id, resource_id=item.id)

    def get_items(self, owner_id: UUID) -> list[ItemDto]:
        repository = ItemsRepository()
        items = repository.for_owner(owner_id=owner_id)
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

    def get(self, item_id: int) -> Item:
        repository = ItemsRepository()
        return repository.get(item_id=item_id)

    def _format_amount(self, price: Money) -> str:
        decimal_points = price.currency.decimal_precision
        formatter = "{0:." + str(decimal_points) + "f}"
        return formatter.format(price.amount)
