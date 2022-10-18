from tests.acceptance.steps import Steps


def test_bought_item_is_no_longer_visible_in_catalog(steps: Steps) -> None:
    steps.add_item(title="Foo", user_uuid=steps.new_user_uuid())

    item = steps.find_item(title="Foo")
    steps.buy(item["id"])
