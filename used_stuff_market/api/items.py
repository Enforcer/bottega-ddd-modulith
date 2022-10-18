from decimal import Decimal
from uuid import UUID

from fastapi import Depends, Header, Response
from fastapi.routing import APIRouter
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session

from used_stuff_market.api.session_deps import get_session
from used_stuff_market.items import Items
from used_stuff_market.shared_kernel.money import Currency, Money

router = APIRouter()


class MoneyData(BaseModel):
    amount: Decimal
    currency: str


class AddItemData(BaseModel):
    title: str
    description: str
    starting_price: MoneyData

    @validator("starting_price")
    def money_validate(cls, v: MoneyData) -> Money:
        return Money(Currency.from_code(v.currency), v.amount)


@router.post("/items")
def add(
    data: AddItemData, user_id: UUID = Header(), session: Session = Depends(get_session)
) -> Response:
    items = Items()
    items.add(**data.dict(), owner_id=user_id)
    session.commit()
    return Response(status_code=204)


@router.get("/items")
def get_items(user_id: UUID = Header()) -> list[dict]:
    items = Items()
    return items.get_items(owner_id=user_id)
