from decimal import Decimal
from enum import StrEnum
from typing import Tuple

import attr
from fastapi import Header, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRouter
from pydantic import BaseModel

from used_stuff_market.negotiations.negotiation import Negotiation, State

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
    _participant_or_403(user_id, payload.buyer_id, payload.seller_id)

    key = (item_id, payload.buyer_id, payload.seller_id)
    if key in _NEGOTIATIONS:
        return JSONResponse(status_code=409, content={})

    initial_state = (
        State.WAITING_FOR_BUYER
        if user_id == payload.seller_id
        else State.WAITING_FOR_SELLER
    )
    negotiation = Negotiation(
        item_id=item_id,
        seller_id=payload.seller_id,
        buyer_id=payload.buyer_id,
        price=payload.price,
        currency=payload.currency,
        state=initial_state,
    )
    _NEGOTIATIONS[key] = negotiation

    return Response(status_code=204)


@router.get("/items/{item_id}/negotiations")
def get(
    item_id: int, buyer_id: int, seller_id: int, user_id: int = Header()
) -> Response:
    _participant_or_403(user_id, buyer_id, seller_id)

    key = (item_id, buyer_id, seller_id)
    try:
        negotiation = _NEGOTIATIONS[key]
    except KeyError:
        return Response(status_code=404)
    else:
        as_dict = {
            key.lstrip("_"): value for key, value in attr.asdict(negotiation).items()
        }
        content = jsonable_encoder(as_dict)
        return JSONResponse(status_code=200, content=content)


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
    _participant_or_403(user_id, payload.buyer_id, payload.seller_id)

    key = (item_id, payload.buyer_id, payload.seller_id)
    try:
        negotiation = _NEGOTIATIONS[key]
    except KeyError:
        return Response(status_code=404)
    else:
        negotiation.counteroffer(
            user_id=user_id, price=payload.price, currency=payload.currency
        )
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
    _participant_or_403(user_id, accepting.buyer_id, accepting.seller_id)

    key = (item_id, accepting.buyer_id, accepting.seller_id)
    try:
        negotiation = _NEGOTIATIONS[key]
    except KeyError:
        return Response(status_code=404)
    else:
        negotiation.accept(user_id=user_id)
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
    _participant_or_403(user_id, breaking_off.buyer_id, breaking_off.seller_id)

    key = (item_id, breaking_off.buyer_id, breaking_off.seller_id)
    try:
        negotiation = _NEGOTIATIONS[key]
    except KeyError:
        return Response(status_code=404)
    else:
        negotiation.accept(user_id=user_id)
        return Response(status_code=204)


def _participant_or_403(user_id: int, buyer_id: int, seller_id: int) -> None:
    if user_id not in (buyer_id, seller_id):
        raise HTTPException(status_code=403)
