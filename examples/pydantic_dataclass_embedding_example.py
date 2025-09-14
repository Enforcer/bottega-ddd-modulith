from dataclasses import fields
from typing import Annotated, Any

from pydantic import Field, AfterValidator
from pydantic.dataclasses import dataclass

from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, composite, Session, MappedColumn


class MyBase(DeclarativeBase):
    pass


def is_digit(value: str) -> str:
    if not value.isdigit():
        raise ValueError(f"{value} is not a valid number!")
    return value


@dataclass
class PostalCode:
    value: Annotated[str, Field(min_length=5, max_length=5), AfterValidator(is_digit)]


def columns_from_dataclass(dataclass: Any) -> list[MappedColumn[Any]]:
    return [
        mapped_column(field.name) for field in fields(dataclass)
    ]


class MyAddress(MyBase):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    postal_code: Mapped[PostalCode] = composite(*columns_from_dataclass(PostalCode))

    def __repr__(self) -> str:
        return f"<MyAddress {self.id=} {self.postal_code=}>"


engine = create_engine("sqlite:///:memory:", echo=True)
MyBase.metadata.create_all(engine)

with engine.connect() as connection:
    session = Session(bind=connection)
    session.execute(insert(MyAddress).values(postal_code=PostalCode(value="12345")))
    result = session.execute(select(MyAddress))
    print(result.scalars().all())
