from datetime import datetime, timedelta
from typing import TypedDict

__all__ = ["Payments", "PaymentDto"]

from uuid import UUID

from used_stuff_market.db import Session
from used_stuff_market.payments.models import Payment
from used_stuff_market.shared_kernel.money import Currency, Money


class PaymentDto(TypedDict):
    uuid: UUID
    amount: Money
    description: str


class Payments:
    def initialize(
        self,
        owner_id: UUID,
        uuid: UUID,
        amount: Money,
        description: str,
    ) -> None:
        now = datetime.utcnow()
        session = Session()
        payment = Payment(
            uuid=uuid,
            owner_id=owner_id,
            created_at=now,
            amount=amount.amount,
            currency=amount.currency.iso_code,
            description=description,
        )
        session.add(payment)
        session.flush()

    def pending(self, owner_id: UUID) -> list[PaymentDto]:
        session = Session()
        payments = session.query(Payment).filter(
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
        session = Session()
        payment = (
            session.query(Payment)
            .filter(Payment.owner_id == str(owner_id), Payment.uuid == str(uuid))
            .one()
        )
        payment.mark_as_finished()
