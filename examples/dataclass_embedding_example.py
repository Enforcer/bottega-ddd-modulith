from dataclasses import dataclass

from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, composite, Session


class MyBase(DeclarativeBase):
    pass


@dataclass
class Point:
    x: int
    y: int


class Segment(MyBase):
    __tablename__ = "segments"

    id: Mapped[int] = mapped_column(primary_key=True)

    start: Mapped[Point] = composite(mapped_column("x1"), mapped_column("y1"))
    end: Mapped[Point] = composite(mapped_column("x2"), mapped_column("y2"))

    def __repr__(self) -> str:
        return f"<Segment {self.id=} {self.start=} {self.end=}>"


engine = create_engine("sqlite:///:memory:", echo=True)
MyBase.metadata.create_all(engine)

with engine.connect() as connection:
    session = Session(bind=connection)
    session.execute(insert(Segment).values(start=Point(0, 0), end=Point(1, 0)))
    result = session.execute(select(Segment))
    print(result.scalars().all())