from uuid import UUID

from fastapi import Header
from fastapi.routing import APIRouter

router = APIRouter()


@router.post("/items/{item_id}/like")
def like(item_id: int, user_id: UUID = Header()) -> None:
    pass


@router.delete("/items/{item_id}/like")
def unlike(item_id: int, user_id: UUID = Header()) -> None:
    pass
