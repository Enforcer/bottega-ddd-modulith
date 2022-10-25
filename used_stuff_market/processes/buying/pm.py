from datetime import datetime, timedelta
from uuid import UUID, uuid4

from used_stuff_market.availability import Availability
from used_stuff_market.db import ScopedSession
from used_stuff_market.negotiations.events import PriceAgreed
from used_stuff_market.payments import Payments
from used_stuff_market.payments.events import PaymentFinalized
from used_stuff_market.processes.buying.events import PaymentTimeout
from used_stuff_market.processes.buying.repository import BuyingProcessManagerStateRepo
from used_stuff_market.processes.buying.state import BuyingProcessState
from used_stuff_market.shared_kernel.event_bus import EventBus, event_bus


def handle_price_agreed(event: PriceAgreed) -> None:
    BuyingProcessManager().price_agreed(event)


def handle_payment_finalized(event: PaymentFinalized) -> None:
    BuyingProcessManager().payment_finalized(event)


def handle_payment_timeout(event: PaymentTimeout) -> None:
    BuyingProcessManager().payment_timeout(event)


def subscribe(an_event_bus: EventBus) -> None:
    an_event_bus.subscribe(PriceAgreed, handle_price_agreed)
    an_event_bus.subscribe(PaymentFinalized, handle_payment_finalized)
    an_event_bus.subscribe(PaymentTimeout, handle_payment_timeout)


subscribe(event_bus)


class PaymentIdGenerator:
    def generate(self) -> UUID:
        return uuid4()


class BuyingProcessManager:
    class DuplicatedEvent(Exception):
        pass

    def __init__(self) -> None:
        self._session = ScopedSession()
        self._repo = BuyingProcessManagerStateRepo()

        self._payment_id_generator = PaymentIdGenerator()
        self._payments = Payments()
        self._availability = Availability()

    def price_agreed(self, event: PriceAgreed) -> None:
        payment_id = self._payment_id_generator.generate()
        state = BuyingProcessState(
            item_id=event.item_id,
            price=event.price,
            payment_id=payment_id,
            buyer_id=event.buyer,
            payment_timeout_at=datetime.utcnow() + timedelta(days=2),
        )
        try:
            self._repo.add(state)
        except BuyingProcessManagerStateRepo.DuplicatedState:
            return

        self._payments.initialize(
            uuid=payment_id,
            amount=event.price,
            owner_id=event.buyer,
            description=f"Payment for item #{event.item_id}",
        )
        self._session.commit()

    def payment_finalized(self, event: PaymentFinalized) -> None:
        state = self._repo.get_for_payment_id(event.payment_id)
        if state.payment_finished_at is not None:
            raise self.DuplicatedEvent

        state.payment_finished_at = datetime.utcnow()
        state.result = "FINISHED"
        self._availability.unregister(resource_id=state.item_id)
        self._session.commit()

    def payment_timeout(self, event: PaymentTimeout) -> None:
        state = self._repo.get_for_payment_id(payment_id=event.payment_id)
        try:
            state.timeout()
        except BuyingProcessState.AlreadyFinished:
            return

        self._payments.cancel(payment_id=event.payment_id)
        self._availability.unlock(resource_id=state.item_id, locked_by=state.buyer_id)
        self._session.commit()
