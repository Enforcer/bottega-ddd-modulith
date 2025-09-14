from sqlalchemy.orm import Session
from used_stuff_market.items import ItemAdded
from used_stuff_market.catalog.models import Product
from used_stuff_market.foundation.event_bus import EventBus


def register_handlers(event_bus: EventBus) -> None:
    def handler(
        event: ItemAdded,
        catalog: Catalog,
        session: Session,
    ) -> None:
        decimal_points = event.starting_price.currency.decimal_precision
        formatter = "{0:." + str(decimal_points) + "f}"

        catalog.add(
            id=event.id,
            data={
                "title": event.title,
                "description": event.description,
                "starting_price": {
                    "amount": formatter.format(event.starting_price.amount),
                    "currency": event.starting_price.currency.iso_code,
                },
            },
        )
        session.commit()

    event_bus.subscribe(ItemAdded, handler)


class Catalog:
    def __init__(self, session: Session) -> None:
        self._session = session

    def search(self, term: str) -> list[dict]:
        products = (
            self._session.query(Product).filter(Product.ts_vector.match(term)).limit(5)
        )
        return [product.data for product in products]

    def add(self, id: int, data: dict) -> None:
        product = Product(id=id, data={**data, "id": id, "sold": False, "likes": 0})
        self._session.add(product)
