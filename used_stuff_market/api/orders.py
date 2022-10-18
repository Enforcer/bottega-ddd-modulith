from uuid import UUID

from fastapi import Header
from fastapi.routing import APIRouter
from pydantic import BaseModel

from used_stuff_market.orders import DeliveryMethod, Orders

router = APIRouter()


class OrderPayload(BaseModel):
    delivery_method: DeliveryMethod


@router.post("/items/{item_id}/orders")
def order(item_id: int, payload: OrderPayload, user_id: UUID = Header()):
    orders = Orders()
    orders.order()
