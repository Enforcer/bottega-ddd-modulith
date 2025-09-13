from sqlalchemy.orm import Session
from used_stuff_market.catalog.models import Product


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
