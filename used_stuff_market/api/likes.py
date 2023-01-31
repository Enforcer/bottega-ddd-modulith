from uuid import UUID

from fastapi import Header
from fastapi.routing import APIRouter

from used_stuff_market.catalog import Catalog
from used_stuff_market.likes import Likes

router = APIRouter()


@router.post("/items/{item_id}/like")
def like(item_id: int, user_id: UUID = Header()) -> None:
    likes = Likes()
    likes.like_item(item_id=item_id, user_id=user_id)


@router.delete("/items/{item_id}/like")
def unlike(item_id: int, user_id: UUID = Header()) -> None:
    likes = Likes()
    likes.unlike_item(item_id=item_id, user_id=user_id)


@router.get("/items/{item_id}/likers")
def likers(item_id: int) -> list[str]:
    likes = Likes()
    return likes.likers(item_id=item_id)
