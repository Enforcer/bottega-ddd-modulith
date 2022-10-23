from used_stuff_market.db import db_session
from used_stuff_market.workers.with_celery import app


@app.task
def increase_likes(item_id: int) -> None:
    from used_stuff_market.catalog import Catalog

    with db_session() as session:
        Catalog().increase_likes(item_id=item_id)
        session.commit()


@app.task
def decrease_likes(item_id: int) -> None:
    from used_stuff_market.catalog import Catalog

    with db_session() as session:
        Catalog().decrease_likes(item_id=item_id)
        session.commit()

