from datetime import datetime, timezone
from typing import TypedDict

from uuid import UUID

from sqlalchemy.orm import Session

from used_stuff_market.payments.models import Payment
from used_stuff_market.shared_kernel.money import Currency, Money


__all__ = ["Payments", "PaymentDto"]


class PaymentDto(TypedDict):
    uuid: UUID
    amount: Money
    description: str


class Payments:
    def __init__(self, session: Session) -> None:
        self._session = session

    def initialize(
        self,
        owner_id: UUID,
        uuid: UUID,
        amount: Money,
        description: str,
    ) -> None:
        now = datetime.now(tz=timezone.utc)
        payment = Payment(
            uuid=uuid,
            owner_id=owner_id,
            created_at=now,
            amount=amount.amount,
            currency=amount.currency.iso_code,
            description=description,
        )
        self._session.add(payment)
        self._session.flush()

    def pending(self, owner_id: UUID) -> list[PaymentDto]:
        payments = self._session.query(Payment).filter(
            Payment.owner_id == str(owner_id), Payment.status == "PENDING"
        )
        return [
            PaymentDto(
                uuid=payment.uuid,
                amount=Money(Currency.from_code(payment.currency), payment.amount),
                description=payment.description,
            )
            for payment in payments
        ]

    def finalize(self, owner_id: UUID, uuid: UUID) -> None:
        payment = (
            self._session.query(Payment)
            .filter(Payment.owner_id == str(owner_id), Payment.uuid == str(uuid))
            .one()
        )
        payment.mark_as_finished()
