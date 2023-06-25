from decimal import Decimal
from enum import StrEnum
from typing import Tuple

from fastapi import Header
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRouter
from pydantic import BaseModel

from used_stuff_market.negotiations.negotiation import Negotiation

router = APIRouter()


# key: (item_id, buyer_id, seller_id)
_NEGOTIATIONS: dict[Tuple[int, int, int], Negotiation] = {}


class Currency(StrEnum):
    USD = "USD"


class NewNegotiation(BaseModel):
    seller_id: int
    buyer_id: int
    price: Decimal
    currency: Currency

    class Config:
        schema_extra = {
            "example": {
                "seller_id": 1,
                "buyer_id": 2,
                "price": "1.99",
                "currency": "USD",
            }
        }


@router.post("/items/{item_id}/negotiations")
def start_negotiation(
    item_id: int, payload: NewNegotiation, user_id: int = Header()
) -> Response:
    # negotiation = Negotiation(...)
    return Response(status_code=204)


@router.get("/items/{item_id}/negotiations")
def get(
    item_id: int, buyer_id: int, seller_id: int, user_id: int = Header()
) -> Response:
    ...
    return JSONResponse(status_code=200, content={})


class CounterOffer(BaseModel):
    seller_id: int
    buyer_id: int
    price: Decimal
    currency: Currency

    class Config:
        schema_extra = {
            "example": {
                "seller_id": 1,
                "buyer_id": 2,
                "price": "1.99",
                "currency": "USD",
            }
        }


@router.post("/items/{item_id}/negotiations/counteroffer")
def counteroffer(
    item_id: int, payload: CounterOffer, user_id: int = Header()
) -> Response:
    ...
    return Response(status_code=204)


class NegotiationToAccept(BaseModel):
    seller_id: int
    buyer_id: int

    class Config:
        schema_extra = {
            "example": {
                "seller_id": 1,
                "buyer_id": 2,
            }
        }


@router.post("/items/{item_id}/negotiations/accept")
def accept(
    item_id: int, accepting: NegotiationToAccept, user_id: int = Header()
) -> Response:
    ...
    return Response(status_code=204)


class NegotiationToBreakOff(BaseModel):
    seller_id: int
    buyer_id: int

    class Config:
        schema_extra = {
            "example": {
                "seller_id": 1,
                "buyer_id": 2,
            }
        }


@router.delete("/items/{item_id}/negotiations")
def break_off(
    item_id: int, breaking_off: NegotiationToBreakOff, user_id: int = Header()
) -> Response:
    ...
    return Response(status_code=204)
