import bcrypt
from lagom import bind_to_container, injectable
from sqlalchemy import select
from sqlalchemy.orm import Session

from used_stuff_market.main.container import context_container
from used_stuff_market.users.models import User


@bind_to_container(context_container)
def register_user(username: str, password: str, session: Session = injectable) -> None:
    session.add(
        User(
            username=username,
            password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
        )
    )
    session.commit()


@bind_to_container(context_container)
def authenticate_user(
    username: str, password: str, session: Session = injectable
) -> bool:
    stmt = select(User).where(User.username == username)
    user = session.execute(stmt).scalars().first()
    if user is None:
        return False

    return bcrypt.checkpw(password.encode(), user.password)
