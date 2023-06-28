from uuid import UUID

from fastapi import Header, Depends
from fastapi.responses import Response
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from used_stuff_market.api.session_deps import get_session
from used_stuff_market.likes.models import Like

router = APIRouter()


@router.post("/items/{item_id}/like")
def like(
    item_id: int, user_id: UUID = Header(), session: Session = Depends(get_session)
) -> Response:
    like = Like(item_id=item_id, liker=user_id)
    session.add(like)
    session.commit()

    return Response(status_code=201)


@router.delete("/items/{item_id}/like")
def unlike(
    item_id: int, user_id: UUID = Header(), session: Session = Depends(get_session)
) -> Response:
    session.query(Like).filter(
        Like.item_id == item_id, Like.liker == str(user_id)
    ).delete()

    session.commit()

    return Response(status_code=204)
