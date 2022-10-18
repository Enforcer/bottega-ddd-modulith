from typing import Iterator

from used_stuff_market.db import Session


def get_session() -> Iterator[Session]:
    a_session = Session()
    try:
        yield a_session
    except Exception:
        raise
    finally:
        Session.remove()
