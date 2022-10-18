from used_stuff_market.catalog.models import Product
from used_stuff_market.db import Session


class Catalog:
    def search(self, term: str) -> list[dict]:
        session = Session()
        products = (
            session.query(Product).filter(Product.__ts_vector__.match(term)).limit(5)
        )
        return [product.data for product in products]

    def add(self, id: int, data: dict) -> None:
        session = Session()
        product = Product(id=id, data={**data, "id": id, "sold": False, "likes": 0})
        session.add(product)
