from uuid import UUID

from fastapi import Header
from fastapi.routing import APIRouter

from used_stuff_market.payments import Payments

router = APIRouter()


@router.get("/payments/pending")
def pending_payments(user_id: UUID = Header()) -> list[dict]:
    pending = Payments().pending(owner_id=user_id)
    return [
        {
            "uuid": payment["uuid"],
            "amount": {
                "amount": payment["amount"].amount,
                "currency": payment["amount"].currency.iso_code,
            },
            "description": payment["description"],
        }
        for payment in pending
    ]
