from fastapi import Depends, FastAPI

from used_stuff_market import db
from used_stuff_market.api import catalog, items, likes, negotations, orders, users
from used_stuff_market.api.session_deps import get_session

app = FastAPI(dependencies=[Depends(get_session)])
app.include_router(items.router)
app.include_router(negotations.router)
app.include_router(catalog.router)
app.include_router(orders.router)
app.include_router(likes.router)
app.include_router(users.router)


@app.on_event("startup")
def migrate() -> None:
    import pymongo

    db.mongo_db["negotiations"].create_index(
        [
            ("item_id", pymongo.ASCENDING),
            ("buyer_id", pymongo.ASCENDING),
            ("seller_id", pymongo.ASCENDING),
        ],
        unique=True,
    )
