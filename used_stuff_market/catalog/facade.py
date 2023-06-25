from used_stuff_market.catalog.models import Product
from used_stuff_market.db import ScopedSession


class Catalog:
    def search(self, term: str) -> list[dict]:
        session = ScopedSession()
        products = session.query(Product).filter(Product.ts_vector.match(term)).limit(5)
        return [product.data for product in products]

    def add(self, id: int, data: dict) -> None:
        session = ScopedSession()
        product = Product(id=id, data={**data, "id": id, "sold": False, "likes": 0})
        session.add(product)

    def increase_likes(self, item_id: int) -> None:
        session = ScopedSession()
        product: Product = session.query(Product).filter(Product.id == item_id).one()
        data = product.data.copy()
        data["likes"] += 1
        product.data = data

    def decrease_likes(self, item_id: int) -> None:
        session = ScopedSession()
        product: Product = session.query(Product).filter(Product.id == item_id).one()
        data = product.data.copy()
        data["likes"] -= 1
        product.data = data
