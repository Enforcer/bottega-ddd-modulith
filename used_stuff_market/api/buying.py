from uuid import UUID

from fastapi import Header, Response
from fastapi.routing import APIRouter
from sqlalchemy import true

from used_stuff_market.catalog import Catalog
from used_stuff_market.db import ScopedSession
from used_stuff_market.items import Items
from used_stuff_market.payments import Payments

router = APIRouter()


@router.post("/items/{item_id}/buy")
def buy_item(item_id: int, user_id: UUID = Header()) -> Response:
    from used_stuff_market.negotiations.models import Negotiation

    session = ScopedSession()
    items = Items()
    item = items.get(item_id=item_id)
    catalog = Catalog()
    catalog.mark_as_bought(item_id=item_id)

    accepted_negotiation = (
        session.query(Negotiation)
        .filter(
            Negotiation.item_id == item_id,
            Negotiation.owner_id == str(item.owner_id),
            Negotiation.buyer_id == str(user_id),
            Negotiation.accepted == true(),
        )
        .first()
    )

    price = accepted_negotiation.offer if accepted_negotiation else item.starting_price

    payments = Payments()
    payments.initialize(
        owner_id=user_id,
        uuid=UUID(int=item_id),
        amount=price,
        description=f"Buying {item.title}",
    )
    session.commit()
    return Response(status_code=200)
