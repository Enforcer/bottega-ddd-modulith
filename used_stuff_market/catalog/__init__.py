from sqlalchemy import Boolean, cast

from used_stuff_market.catalog.models import Product
from used_stuff_market.db import ScopedSession


class Catalog:
    def search(self, term: str) -> list[dict]:
        session = ScopedSession()
        products = (
            session.query(Product)
            .filter(
                Product.search.like(f"%{term}%"),
                cast(Product.data["sold"], Boolean) == False,
            )
            .limit(5)
        )
        return [product.data for product in products]

    def add(self, id: int, data: dict) -> None:
        session = ScopedSession()
        product = Product(
            id=id,
            search=f"{data['title']} {data['description']}",
            data={
                **data,
                "id": id,
                "sold": False,
                "likes": 0,
            },
        )
        session.add(product)

    def mark_as_bought(self, item_id: int) -> None:
        session = ScopedSession()
        product = session.query(Product).get(item_id)
        product.data = product.data | {"sold": True}
        session.commit()

    def increase_likes(self, item_id: int) -> None:
        session = ScopedSession()
        product = session.query(Product).get(item_id)
        product.data = product.data | {"likes": product.data["likes"] + 1}

    def decrease_likes(self, item_id: int) -> None:
        session = ScopedSession()
        product = session.query(Product).get(item_id)
        product.data = product.data | {"likes": product.data["likes"] - 1}
