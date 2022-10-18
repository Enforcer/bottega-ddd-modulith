from datetime import datetime, timedelta
from uuid import UUID

from used_stuff_market.availability.models import Resource
from used_stuff_market.db import Session


class Availability:
    class AlreadyLocked(Exception):
        pass

    class LockedBySomeoneElse(Exception):
        pass

    def register(self, owner_id: UUID, resource_id: int) -> None:
        session = Session()
        session.add(
            Resource(
                id=resource_id,
                owner_id=str(owner_id),
                created_at=datetime.utcnow(),
            )
        )
        session.flush()

    def unregister(self, resource_id: int) -> None:
        session = Session()
        session.query(Resource).filter(Resource.id == resource_id).delete()

    def lock(
        self, resource_id: int, lock_for: UUID, duration: timedelta = timedelta(days=1)
    ) -> None:
        session = Session()
        now = datetime.utcnow()
        updated_rows = (
            session.query(Resource)
            .filter(
                Resource.id == resource_id,
                (
                    (Resource.locked_by.is_(None) & Resource.locked_to.is_(None))
                    | (Resource.locked_by == str(lock_for))
                    | (Resource.locked_to < now)
                ),
            )
            .update(
                {
                    Resource.locked_by: str(lock_for),
                    Resource.locked_to: now + duration,
                }
            )
        )
        if updated_rows != 1:
            raise Availability.AlreadyLocked

    def unlock(self, resource_id: int, locked_by: UUID) -> None:
        session = Session()
        updated_rows = (
            session.query(Resource)
            .filter(
                Resource.id == resource_id,
                Resource.locked_by == str(locked_by),
            )
            .update(
                {
                    Resource.locked_by: None,
                    Resource.locked_to: None,
                }
            )
        )
        if updated_rows != 1:
            raise Availability.LockedBySomeoneElse
