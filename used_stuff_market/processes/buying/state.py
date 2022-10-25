from datetime import datetime
from typing import Literal
from uuid import UUID

import attr

from used_stuff_market.shared_kernel.money import Money


@attr.s(auto_attribs=True)
class BuyingProcessState:
    class AlreadyFinished(Exception):
        pass

    item_id: int
    price: Money
    payment_id: UUID
    buyer_id: UUID
    payment_timeout_at: datetime | None = None
    payment_finished_at: datetime | None = None
    result: Literal["FINISHED", "TIMEOUT"] | None = None

    def timeout(self) -> None:
        if self.result is None:
            self.result = "TIMEOUT"
        else:
            raise self.AlreadyFinished
