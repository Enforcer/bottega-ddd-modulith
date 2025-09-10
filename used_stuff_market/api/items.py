from decimal import Decimal
from typing import Self
from uuid import UUID

from fastapi import Depends, Header, Response
from fastapi.routing import APIRouter
from pydantic import BaseModel, model_validator
from sqlalchemy.orm import Session

from used_stuff_market.api.session_deps import get_session
from used_stuff_market.items import Items
from used_stuff_market.utils import Currency, Money, validate_amount

router = APIRouter()


class MoneyData(BaseModel):
    amount: Decimal
    currency: str

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        try:
            currency = Currency.from_code(self.currency)
        except ValueError:
            raise
        else:
            self.amount = validate_amount(currency, self.amount)

        return self

    def to_money(self) -> Money:
        return Money(Currency.from_code(self.currency), self.amount)


class AddItemData(BaseModel):
    title: str
    description: str
    starting_price: MoneyData


@router.post("/items")
def add(
    data: AddItemData, user_id: UUID = Header(), session: Session = Depends(get_session)
) -> Response:
    items = Items()
    items.add(
        **data.model_dump(exclude={"starting_price"}),
        starting_price=data.starting_price.to_money(),
        owner_id=user_id,
    )
    session.commit()
    return Response(status_code=204)


@router.get("/items")
def get_items(user_id: UUID = Header()) -> list[dict]:
    items = Items()
    return items.get_items(owner_id=user_id)  # type: ignore
