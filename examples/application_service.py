# examples/application_service.py
from typing import TypedDict
from uuid import UUID

from used_stuff_market.utils import Money


class ProductDto(TypedDict):
    ...


class ItemsManagementService:
    def add(
        self, owner_id: UUID, title: str, description: str, starting_price: Money
    ) -> None:
        ...

    def get_items(self, owner_id: UUID) -> list[ProductDto]:
        ...


class ItemsExternalUpdatesService:
    def mark_as_sold(self, owner_id, item_id: int) -> None:
        ...
