from used_stuff_market.db import db_session
from used_stuff_market.workers.with_celery import app


@app.task
def catalog_task() -> None:
    # To run: catalog_task.delay(<argument1>, <argument2>)...
    with db_session():
        pass
