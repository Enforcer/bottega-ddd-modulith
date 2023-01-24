import bcrypt
from sqlalchemy import select

from used_stuff_market.db import ScopedSession
from used_stuff_market.users.models import User


def register_user(username: str, password: str) -> None:
    session = ScopedSession()
    session.add(
        User(
            username=username,
            password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
        )
    )
    session.commit()


def authenticate_user(username: str, password: str) -> bool:
    session = ScopedSession()
    stmt = select(User).where(User.username == username)
    user = session.execute(stmt).scalars().first()
    if user is None:
        return False

    return bcrypt.checkpw(password.encode(), user.password)
