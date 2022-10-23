from tests.acceptance.steps import Steps


def test_liked_item_with_0_likes_gets_1_like_available_publicly(steps: Steps) -> None:
    steps.add_item(title="Bar", user_uuid=steps.new_user_uuid())
    item = steps.find_item(title="Bar")
    assert item["likes"] == 0
    steps.like(item_id=item["id"], user_uuid=steps.new_user_uuid())

    changed_item = steps.find_item(title="Bar")
    assert changed_item["likes"] == 1


def test_likes_then_unliked_item_has_0_likes(steps: Steps) -> None:
    steps.add_item(title="Nuts", user_uuid=steps.new_user_uuid())
    item = steps.find_item(title="Nuts")
    liker = steps.new_user_uuid()
    steps.like(item_id=item["id"], user_uuid=liker)

    steps.unlike(item_id=item["id"], user_uuid=liker)

    changed_item = steps.find_item(title="Nuts")
    assert changed_item["likes"] == 0


def test_liking_twice_has_no_effect(steps: Steps) -> None:
    steps.add_item(title="Baz", user_uuid=steps.new_user_uuid())
    item = steps.find_item(title="Baz")

    liker = steps.new_user_uuid()
    steps.like(item_id=item["id"], user_uuid=liker)
    steps.like(item_id=item["id"], user_uuid=liker)

    changed_item = steps.find_item(title="Baz")
    assert changed_item["likes"] == 1


def test_unliking_twice_has_no_effect(steps: Steps) -> None:
    steps.add_item(title="Yesterday", user_uuid=steps.new_user_uuid())
    item = steps.find_item(title="Yesterday")
    liker = steps.new_user_uuid()
    steps.like(item_id=item["id"], user_uuid=liker)

    steps.unlike(item_id=item["id"], user_uuid=liker)
    steps.unlike(item_id=item["id"], user_uuid=liker)

    changed_item = steps.find_item(title="Yesterday")
    assert changed_item["likes"] == 0
