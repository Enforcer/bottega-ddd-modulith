from used_stuff_market.db import ScopedSession


class BuyingProcessManagerStateRepo:
    def __init__(self) -> None:
        self._session = ScopedSession()

    def get_for_item(self, item_id: int) -> None: ...
