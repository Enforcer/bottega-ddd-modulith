from decimal import Decimal
from uuid import UUID

from fastapi import Header, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound

from used_stuff_market.db import ScopedSession
from used_stuff_market.items import Items
from used_stuff_market.negotiations.models import Negotiation

router = APIRouter()


class OfferData(BaseModel):
    amount: Decimal
    currency: str


@router.post("/items/{item_id}/offer")
def offer(item_id: int, offer_data: OfferData, user_id: UUID = Header()) -> Response:
    session = ScopedSession()
    items = Items()
    item = items.get(item_id=item_id)
    if item.owner_id == user_id:
        return JSONResponse(
            status_code=400, content={"error": "You negotiate your own item."}
        )

    if offer_data.currency != item.starting_price.currency.iso_code:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Currency of the offer must match the currency of the item."
            },
        )

    negotiation = Negotiation(
        item_id=item_id,
        owner_id=item.owner_id,
        buyer_id=user_id,
        amount=offer_data.amount,
        currency=offer_data.currency,
        accepted=False,
    )
    session.add(negotiation)
    session.commit()

    return Response(status_code=200)


@router.get("/items/{item_id}/offers")
def list_offer(item_id: int, user_id: UUID = Header()) -> JSONResponse:
    session = ScopedSession()
    items = Items()
    try:
        item = items.get(item_id=item_id)
    except NoResultFound:
        return JSONResponse(status_code=404, content={"error": "Item not found."})

    if item.owner_id != user_id:
        return JSONResponse(
            status_code=401, content={"error": "You can't see offers for other users."}
        )

    offers = session.query(Negotiation).filter(Negotiation.item_id == item_id).all()
    return JSONResponse(
        status_code=200,
        content=[
            {
                "id": str(offer.buyer_id),
                "amount": str(offer.amount),
                "currency": offer.currency,
                "accepted": offer.accepted,
            }
            for offer in offers
        ],
    )


@router.post("/items/{item_id}/offers/{id}/accept")
def accept_offer(item_id: int, id: UUID, user_id: UUID = Header()) -> None:
    session = ScopedSession()
    negotiation = (
        session.query(Negotiation)
        .filter(
            Negotiation.item_id == item_id,
            Negotiation.buyer_id == str(id),
        )
        .first()
    )
    if negotiation is None:
        return JSONResponse(status_code=404, content={"error": "Offer not found."})

    if negotiation.owner_id != user_id:
        return JSONResponse(
            status_code=401,
            content={"error": "You can't accept offers for other users."},
        )

    if negotiation.accepted:
        return JSONResponse(
            status_code=400, content={"error": "Offer already accepted."}
        )
    negotiation.accepted = True
    session.commit()
