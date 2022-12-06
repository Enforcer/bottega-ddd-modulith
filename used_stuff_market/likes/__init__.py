from uuid import UUID

from sqlalchemy.exc import IntegrityError

from used_stuff_market.db import ScopedSession
from used_stuff_market.catalog.events import ItemLiked, ItemUnliked
from used_stuff_market.likes.models import Like
from used_stuff_market.shared_kernel.event_bus import event_bus


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

        event = ItemLiked(item_id=item_id)
        event_bus.publish(event)

    def unlike(self, liker: UUID, item_id: int) -> None:
        session = ScopedSession()
        removed = (
            session.query(Like)
            .filter(Like.item_id == item_id, Like.liker == str(liker))
            .delete()
        )

        if removed > 0:
            event = ItemUnliked(item_id=item_id)
            event_bus.publish(event)
