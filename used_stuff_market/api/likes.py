from uuid import UUID

from fastapi import Depends, Header, Response
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from used_stuff_market.api.session_deps import get_session
from used_stuff_market.likes import Likes

router = APIRouter()


@router.post("/items/{item_id}/like")
def like(
    item_id: int, user_id: UUID = Header(), session: Session = Depends(get_session)
) -> Response:
    likes = Likes()
    likes.like(liker=user_id, item_id=item_id)

    session.commit()

    return Response(status_code=201)


@router.delete("/items/{item_id}/like")
def unlike(
    item_id: int, user_id: UUID = Header(), session: Session = Depends(get_session)
) -> Response:
    likes = Likes()
    likes.unlike(liker=user_id, item_id=item_id)

    session.commit()

    return Response(status_code=204)
