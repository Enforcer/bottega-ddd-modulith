import httpx


def test_api() -> None:
    response = httpx.get("https://jsonplaceholder.typicode.com/posts/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "userId": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
    }
