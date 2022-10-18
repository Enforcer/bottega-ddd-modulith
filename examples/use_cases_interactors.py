# examples/use_cases_interactors.py
from typing import TypedDict
from uuid import UUID

from used_stuff_market.shared_kernel.money import Money


class ProductDto(TypedDict):
    ...


class AddingItemUseCase:
    def __call__(
        self, owner_id: UUID, title: str, description: str, starting_price: Money
    ) -> None:
        ...


class GettingItems:
    def __call__(self, owner_id: UUID) -> list[ProductDto]:
        ...


class MarkingAsSold:
    def __call__(self, owner_id, item_id: int) -> None:
        ...
