import abc
from dataclasses import dataclass
from decimal import Decimal
from typing import TypedDict, Any
from uuid import UUID, uuid4

from fastapi import FastAPI, Depends
from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

from used_stuff_market.items import Item
from used_stuff_market.utils import Money, Currency

app = FastAPI()


def get_repository() -> "ItemsRepository":
    return SqlItemsRepository()


def get_adding_item(
    repository: "ItemsRepository" = Depends(get_repository),
) -> "AddingItemsUseCase":
    return Items(repository=repository)


def authenticated_user_id() -> UUID:
    """Fake pretending to be doing some authentication."""
    return uuid4()


class MoneyPayload(Money):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        def convert(argument: Any) -> Money:
            if not isinstance(argument, dict):
                raise ValueError("Expected a dict")
            elif "amount" not in argument:
                raise ValueError("Missing 'amount' key")
            elif "currency" not in argument:
                raise ValueError("Missing 'currency' key")
            return Money(
                Currency.from_code(argument["currency"]), Decimal(argument["amount"])
            )

        return core_schema.no_info_plain_validator_function(convert)


class AddItemPayload(BaseModel):
    title: str
    description: str
    starting_price: MoneyPayload


@app.post("/items")
def add_item(
    payload: AddItemPayload,
    user_id: UUID = Depends(authenticated_user_id),
    adding_item: "AddingItemsUseCase" = Depends(get_adding_item),
) -> Any:
    dto = adding_item.add(
        owner_id=user_id,
        title=payload.title,
        description=payload.description,
        starting_price=payload.starting_price,
    )
    return dto


@dataclass(frozen=True)
class MoneyDto(TypedDict):
    amount: str
    currency: str


@dataclass(frozen=True)
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
        return ItemDto(
            id=item.id,
            title=item.title,
            description=item.description,
            starting_price={
                "amount": str(item.starting_price.amount),
                "currency": item.starting_price.currency.iso_code,
            },
        )


class SqlItemsRepository(ItemsRepository):
    """Fake pretending to store items in the database."""

    def __init__(self) -> None:
        self._records: list[Item] = []

    def add(self, item: Item) -> None:
        self._records.append(item)


if __name__ == "__main__":
    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        response = test_client.post(
            "/items",
            json={
                "title": "Foo",
                "description": "Bar",
                "starting_price": {"amount": "19.99", "currency": "USD"},
            },
        )
    assert response.status_code == 200
    print("All good")
