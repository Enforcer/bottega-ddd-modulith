from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from used_stuff_market.users.registration import authenticate_user, register_user

router = APIRouter()


class UserCredentials(BaseModel):
    username: str
    password: str


@router.post("/users")
def create_user(payload: UserCredentials) -> None:
    register_user(payload.username, payload.password)


@router.post("/users/login")
def login_user(payload: UserCredentials) -> dict:
    if authenticate_user(payload.username, payload.password):
        return {"message": "Logged in successfully"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
