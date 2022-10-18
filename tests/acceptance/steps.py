from uuid import UUID, uuid4

import attr
from fastapi.testclient import TestClient


@attr.s(auto_attribs=True)
class Steps:
    _client: TestClient

    def add_item(self, user_uuid: UUID, title: str = "Socks", description: str = "Cool socks with trendy print!") -> None:
        response = self._client.post("/items", json={
            "title": title,
            "description": description,
            "starting_price": {
                "amount": "15.99",
                "currency": "USD",
            }
        }, headers={"user-id": str(user_uuid)})
        assert response.status_code == 204, response.json()

    def find_item(self, title: str) -> dict | None:
        response = self._client.get(f"/catalog/search/{title}")
        assert response.status_code == 200, (response.status_code, response.json())
        results = response.json()
        return results[0]

    @staticmethod
    def new_user_uuid() -> UUID:
        return uuid4()

    def buy(self, item_id: int) -> None:
        pass

    def like(self, item_id: int, user_uuid: UUID):
        raise NotImplementedError()
