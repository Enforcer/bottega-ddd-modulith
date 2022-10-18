import pytest

from tests.acceptance.steps import Steps


@pytest.mark.skip("Not implemented")
def test_liked_item_with_0_likes_gets_1_like_available_publicly(steps: Steps) -> None:
    steps.add_item(title="Bar", user_uuid=steps.new_user_uuid())
    item = steps.find_item(title="Bar")
    assert item["likes"] == 0
    steps.like(item_id=item["id"], user_uuid=steps.new_user_uuid())

    changed_item = steps.find_item(title="Bar")
    assert changed_item["likes"] == 1
