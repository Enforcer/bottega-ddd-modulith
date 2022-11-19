from used_stuff_market.db import db_session
from used_stuff_market.workers.with_celery import app
from used_stuff_market.catalog.facade import Catalog


@app.task
def increase_likes(item_id: int) -> None:
    with db_session() as session:
        Catalog().increase_likes(item_id=item_id)
        session.commit()


@app.task
def decrease_likes(item_id: int) -> None:
    with db_session() as session:
        Catalog().decrease_likes(item_id=item_id)
        session.commit()

