from typing import Iterator

from sqlalchemy.orm import Session

from used_stuff_market.db import db_session


def get_session() -> Iterator[Session]:
    with db_session() as session:
        yield session
