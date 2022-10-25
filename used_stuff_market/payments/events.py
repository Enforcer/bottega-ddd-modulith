from uuid import UUID

from attr import define


@define(frozen=True)
class PaymentFinalized:
    payment_id: UUID
