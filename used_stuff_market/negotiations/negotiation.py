from decimal import Decimal


class Negotiation:
    def __init__(self, item_id: int, seller_id: int, buyer_id: int) -> None:
        self._item_id = item_id
        self._seller_id = seller_id
        self._buyer_id = buyer_id

    def accept(self, user_id: int) -> None:
        pass

    def break_off(self, user_id: int) -> None:
        pass

    def counteroffer(self, user_id: int, price: Decimal, currency: str) -> None:
        pass
