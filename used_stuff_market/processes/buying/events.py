from uuid import UUID

from attr import define


@define(frozen=True)
class PaymentTimeout:
    """We assume that timeouts are implemented under processes."""

    payment_id: UUID
