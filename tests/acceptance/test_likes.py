import time

import pytest
from celery import Celery
from celery.contrib.testing.worker import TestWorkController

from tests.acceptance.steps import Steps
from used_stuff_market.workers.with_celery import app


@pytest.fixture()
def celery_app() -> Celery:
    return app


@pytest.fixture()
def celery_worker_parameters() -> dict:
    return {
        "perform_ping_check": False,
    }


@pytest.fixture(autouse=True)
def tasks_worker(celery_worker: TestWorkController) -> None:
    pass


"""
These test are meant to test our app end-to-end via API, so we emulate the whole flow
using celery worker that gets spun in a separate thread.

Also, since now there's asynchronous processing in the background due to this change,
we rewrite our assertions so they retry few times, so the task gets a chance to execute.

Other approaches involve patching task's delay method so it calls the task in place
or reconfigure Celery to use TASK_ALWAYS_EAGER (so tasks are executed also in memory).
"""


def test_liked_item_with_0_likes_gets_1_like_available_publicly(steps: Steps) -> None:
    steps.add_item(title="Bar", user_uuid=steps.new_user_uuid())
    item = steps.find_item(title="Bar")
    assert item["likes"] == 0
    steps.like(item_id=item["id"], user_uuid=steps.new_user_uuid())

    _assert_has_n_likes_with_retry(steps=steps, title="Bar", expected_likes=1)


def test_likes_then_unliked_item_has_0_likes(steps: Steps) -> None:
    steps.add_item(title="Nuts", user_uuid=steps.new_user_uuid())
    item = steps.find_item(title="Nuts")
    liker = steps.new_user_uuid()
    steps.like(item_id=item["id"], user_uuid=liker)

    steps.unlike(item_id=item["id"], user_uuid=liker)

    _assert_has_n_likes_with_retry(steps=steps, title="Nuts", expected_likes=0)


def test_liking_twice_has_no_effect(steps: Steps) -> None:
    steps.add_item(title="Baz", user_uuid=steps.new_user_uuid())
    item = steps.find_item(title="Baz")

    liker = steps.new_user_uuid()
    steps.like(item_id=item["id"], user_uuid=liker)
    steps.like(item_id=item["id"], user_uuid=liker)

    _assert_has_n_likes_with_retry(steps=steps, title="Baz", expected_likes=1)


def test_unliking_twice_has_no_effect(steps: Steps) -> None:
    steps.add_item(title="Yesterday", user_uuid=steps.new_user_uuid())
    item = steps.find_item(title="Yesterday")
    liker = steps.new_user_uuid()
    steps.like(item_id=item["id"], user_uuid=liker)

    steps.unlike(item_id=item["id"], user_uuid=liker)
    steps.unlike(item_id=item["id"], user_uuid=liker)

    _assert_has_n_likes_with_retry(steps=steps, title="Yesterday", expected_likes=0)


def _assert_has_n_likes_with_retry(
    steps: Steps, title: str, expected_likes: int, timeout: int = 3
) -> None:
    def _get_number_of_likes() -> int:
        changed_item = steps.find_item(title=title)
        return int(changed_item["likes"])

    likes = _get_number_of_likes()
    if likes == expected_likes:
        return

    start = time.time()
    while time.time() - start < timeout:
        likes = _get_number_of_likes()
        if likes != expected_likes:
            time.sleep(0.05)
            continue
        else:
            break

    assert likes == expected_likes
