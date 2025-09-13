from typing import ContextManager

from sqlalchemy import text
from sqlalchemy.orm import Session

from used_stuff_market.workers.with_celery import app
from used_stuff_market.main.container import container


@app.task  # type: ignore
def catalog_task() -> None:
    # To run: catalog_task.delay(<argument1>, <argument2>)...
    with container[ContextManager[Session]] as session:  # type: ignore
        print(session.execute(text("SELECT NOW()")).scalar())
