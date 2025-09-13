from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from used_stuff_market.availability.models import Resource


class Availability:
    class AlreadyLocked(Exception):
        pass

    class LockedBySomeoneElse(Exception):
        pass

    def __init__(self, session: Session) -> None:
        self._session = session

    def register(self, owner_id: UUID, resource_id: int) -> None:
        self._session.add(
            Resource(
                id=resource_id,
                owner_id=str(owner_id),
                created_at=datetime.now(timezone.utc),
            )
        )
        self._session.flush()

    def unregister(self, resource_id: int) -> None:
        self._session.query(Resource).filter(Resource.id == resource_id).delete()

    def lock(
        self, resource_id: int, lock_for: UUID, duration: timedelta = timedelta(days=1)
    ) -> None:
        now = datetime.now(tz=timezone.utc)
        updated_rows = (
            self._session.query(Resource)
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
        updated_rows = (
            self._session.query(Resource)
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
