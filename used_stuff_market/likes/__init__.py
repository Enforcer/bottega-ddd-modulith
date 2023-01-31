from uuid import UUID

from sqlalchemy import select

from used_stuff_market.catalog import Catalog
from used_stuff_market.db import ScopedSession
from used_stuff_market.likes.models import Like


class Likes:
    def like_item(self, item_id: int, user_id: UUID) -> None:
        session = ScopedSession()
        session.add(Like(item_id=item_id, liker=user_id))
        session.flush()
        catalog = Catalog()
        catalog.increase_likes(item_id=item_id)
        session.commit()

    def unlike_item(self, item_id: int, user_id: UUID) -> None:
        session = ScopedSession()
        stmt = Like.__table__.delete().where(
            Like.item_id == item_id, Like.liker == user_id
        )
        result = session.execute(stmt)
        if result.rowcount == 1:
            catalog = Catalog()
            catalog.decrease_likes(item_id=item_id)
            session.commit()

    def likers(self, item_id: int) -> list[str]:
        from used_stuff_market.users.models import User

        session = ScopedSession()
        stmt = select(User.username).where(
            User.id.in_(select(Like.liker).where(Like.item_id == item_id).subquery())
        )
        return session.execute(stmt).scalars().all()
