from decimal import Decimal
from typing import Tuple

import attr
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from used_stuff_market.negotiations.negotiation import Negotiation, State


class NegotiationRepository:
    class NotFound(Exception):
        pass

    class AlreadyExists(Exception):
        pass

    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    def create(self, negotiation: Negotiation) -> None:
        _filter, as_dict = self._to_filter_and_dict(negotiation)
        try:
            self._collection.insert_one(as_dict)
        except DuplicateKeyError:
            raise self.AlreadyExists()

    def get(self, item_id: int, buyer_id: int, seller_id: int) -> Negotiation:
        filter = {"item_id": item_id, "buyer_id": buyer_id, "seller_id": seller_id}
        as_dict = self._collection.find_one(filter)
        if as_dict is None:
            raise self.NotFound()
        return Negotiation(
            item_id=as_dict["item_id"],
            seller_id=as_dict["seller_id"],
            buyer_id=as_dict["buyer_id"],
            state=State(as_dict["state"]),
            price=Decimal(as_dict["price"]),
            currency=as_dict["currency"],
        )

    def update(self, negotiation: Negotiation) -> None:
        filter, as_dict = self._to_filter_and_dict(negotiation)
        result = self._collection.update_one(filter, {"$set": as_dict}, upsert=False)
        if result.modified_count == 0:
            raise self.NotFound()

    def _to_filter_and_dict(self, negotiation: Negotiation) -> Tuple[dict, dict]:
        as_dict = {
            key.lstrip("_"): value for key, value in attr.asdict(negotiation).items()
        }
        as_dict["price"] = str(as_dict["price"])
        filter = {
            "item_id": as_dict["item_id"],
            "buyer_id": as_dict["buyer_id"],
            "seller_id": as_dict["seller_id"],
        }
        return filter, as_dict
