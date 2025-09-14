from used_stuff_market.negotiations.events import PriceAgreed
from used_stuff_market.processes.buying.repository import BuyingProcessManagerStateRepo


def handle_price_agreed(event: PriceAgreed) -> None:
    BuyingProcessManager().price_agreed(event)


class BuyingProcessManager:
    def __init__(self) -> None:
        self._repo = BuyingProcessManagerStateRepo()

    def price_agreed(self, event: PriceAgreed) -> None: ...
