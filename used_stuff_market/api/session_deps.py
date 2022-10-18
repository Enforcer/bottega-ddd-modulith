from typing import Iterator

from used_stuff_market.db import Session, db_session


def get_session() -> Iterator[Session]:
    with db_session() as session:
        yield session
