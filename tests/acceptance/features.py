from tests.acceptance.app_client import AppClient


class FeatureObject:
    def __init__(self, app_client: AppClient) -> None:
        self._app_client = app_client


class Users(FeatureObject):
    def register(self, username: str, password: str = "foo") -> None:
        self._app_client.register(username=username, password=password)

    def login(self, username: str, password: str = "foo") -> str:
        return self._app_client.login(username=username, password=password)


class Items(FeatureObject):
    def add(self, title: str, description: str, price: int, as_user: str) -> None:
        self._app_client.add_item(
            title=title, description=description, price=price, user_token=as_user
        )


class Likes(FeatureObject):
    def like(self, item_id: int, as_user: str) -> None:
        self._app_client.like(item_id=item_id, user_token=as_user)

    def get_likers(self, item_id: int, as_user: str) -> list[str]:
        return self._app_client.get_likers(item_id=item_id, user_token=as_user)


class Buying(FeatureObject):
    def buy(self, item_id: int, as_user: str) -> None:
        self._app_client.buy(item_id=item_id, user_token=as_user)


class Payments(FeatureObject):
    def get_pending(self, as_user: str) -> list[dict]:
        return self._app_client.get_pending_payments(user_token=as_user)


class Catalog(FeatureObject):
    def search(self, as_user: str, term: str) -> list[dict]:
        return self._app_client.search(term=term, user_token=as_user)


class Negotiations(FeatureObject):
    def start(
        self, item_id: int, offer: int, as_user: str, expect_to_fail: bool = False
    ) -> None:
        expected_code = 400 if expect_to_fail else 200
        self._app_client.start_negotiation(
            item_id=item_id,
            offer=offer,
            user_token=as_user,
            expected_code=expected_code,
        )

    def list(
        self, item_id: int, as_user: str, expect_to_fail: bool = False
    ) -> list[dict]:
        expected_code = 401 if expect_to_fail else 200
        return self._app_client.get_negotiations(
            item_id=item_id, user_token=as_user, expected_code=expected_code
        )

    def accept(
        self, item_id: int, offer_id: int, as_user: str, expect_to_fail: bool = False
    ) -> None:
        expected_code = 401 if expect_to_fail else 200
        self._app_client.accept_negotiation(
            item_id=item_id,
            offer_id=offer_id,
            user_token=as_user,
            expected_code=expected_code,
        )
