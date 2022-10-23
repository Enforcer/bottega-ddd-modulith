from uuid import UUID

from sqlalchemy.exc import IntegrityError

from used_stuff_market.catalog import Catalog
from used_stuff_market.db import ScopedSession
from used_stuff_market.likes.models import Like


class Likes:
    def like(self, liker: UUID, item_id: int) -> None:
        session = ScopedSession()
        like = Like(item_id=item_id, liker=liker)
        session.add(like)
        try:
            session.flush()
        except IntegrityError:  # already have such a like
            session.rollback()
            return

        catalog = Catalog()
        catalog.increase_likes(item_id=item_id)

    def unlike(self, liker: UUID, item_id: int) -> None:
        session = ScopedSession()
        session.query(Like).filter(
            Like.item_id == item_id, Like.liker == str(liker)
        ).delete()

        catalog = Catalog()
        catalog.decrease_likes(item_id=item_id)
