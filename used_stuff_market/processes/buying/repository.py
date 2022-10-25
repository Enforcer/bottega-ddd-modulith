from uuid import UUID

from sqlalchemy.exc import IntegrityError

from used_stuff_market.db import ScopedSession
from used_stuff_market.processes.buying.state import BuyingProcessState


class BuyingProcessManagerStateRepo:
    class DuplicatedState(Exception):
        pass

    def __init__(self) -> None:
        self._session = ScopedSession()

    def add(self, state: BuyingProcessState) -> None:
        self._session.add(state)
        try:
            self._session.flush()
        except IntegrityError:
            raise self.DuplicatedState

    def get_for_item(self, item_id: int) -> BuyingProcessState:
        state: BuyingProcessState = (
            self._session.query(BuyingProcessState)
            .filter(BuyingProcessState.item_id == item_id)
            .with_for_update()
            .one()
        )
        return state

    def get_for_payment_id(self, payment_id: UUID) -> BuyingProcessState:
        state: BuyingProcessState = (
            self._session.query(BuyingProcessState)
            .filter(BuyingProcessState.payment_id == payment_id.hex)
            .with_for_update()
            .one()
        )
        return state
