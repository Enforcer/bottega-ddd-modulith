from datetime import timedelta
from typing import Iterator, ContextManager
from uuid import uuid4

import pytest
from lagom import Container

from used_stuff_market.availability import Availability
from sqlalchemy.orm import Session


def test_locking_locked_resource_raises_exception(
    resource_id: int, availability: Availability
) -> None:
    lock_for_party = uuid4()
    availability.lock(resource_id=resource_id, lock_for=lock_for_party)

    with pytest.raises(Availability.AlreadyLocked):
        availability.lock(resource_id=resource_id, lock_for=uuid4())


def test_same_locking_for_the_same_party_is_reentrant(
    resource_id: int, availability: Availability
) -> None:
    lock_for_party = uuid4()
    availability.lock(resource_id=resource_id, lock_for=lock_for_party)

    try:
        availability.lock(resource_id=resource_id, lock_for=lock_for_party)
    except Availability.AlreadyLocked:
        pytest.fail("Should not fail")


def test_locks_by_someone_else_after_lock_expires(
    resource_id: int, availability: Availability
) -> None:
    lock_for_party = uuid4()
    another_party = uuid4()
    availability.lock(
        resource_id=resource_id, lock_for=lock_for_party, duration=timedelta(seconds=0)
    )
    availability.lock(resource_id=resource_id, lock_for=another_party)


def test_unlocked_can_be_locked_again(
    resource_id: int, availability: Availability
) -> None:
    lock_for_party = uuid4()
    availability.lock(resource_id=resource_id, lock_for=lock_for_party)
    availability.unlock(resource_id=resource_id, locked_by=lock_for_party)

    try:
        availability.lock(resource_id=resource_id, lock_for=uuid4())
    except Availability.AlreadyLocked:
        pytest.fail("Should not raise an exception")


def test_unlocking_by_other_party_raises_exception(
    resource_id: int, availability: Availability
) -> None:
    lock_for_party = uuid4()
    availability.lock(resource_id=resource_id, lock_for=lock_for_party)

    with pytest.raises(Availability.LockedBySomeoneElse):
        availability.unlock(resource_id=resource_id, locked_by=uuid4())


def test_expired_lock_can_be_release_without_exception(
    resource_id: int, availability: Availability
) -> None:
    lock_for_party = uuid4()
    availability.lock(
        resource_id=resource_id, lock_for=lock_for_party, duration=timedelta(seconds=0)
    )

    try:
        availability.unlock(resource_id=resource_id, locked_by=lock_for_party)
    except Exception:
        pytest.fail("Should not raise an exception")


@pytest.fixture()
def availability(container: Container) -> Iterator[Availability]:
    with container[ContextManager[Session]] as session:  # type: ignore
        yield Availability(session)


ids = iter(range(100_000, 200_000))


@pytest.fixture()
def resource_id(availability: Availability) -> int:
    resource_id = next(ids)
    availability.register(owner_id=uuid4(), resource_id=resource_id)
    return resource_id
