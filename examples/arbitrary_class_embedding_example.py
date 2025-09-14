from sqlalchemy import create_engine, Integer, String, insert, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, composite, Session


class MyBase(DeclarativeBase):
    pass


class Weight:
    def __init__(self, amount: int, unit: str) -> None:
        self.amount = amount
        self.unit = unit

    def __composite_values__(self) -> tuple[int, str]:
        return self.amount, self.unit

    def __repr__(self) -> str:
        return f"<Weight {self.amount=} {self.unit=}>"


class Weights(MyBase):
    __tablename__ = "weights"

    id: Mapped[int] = mapped_column(primary_key=True)
    weight: Mapped[Weight] = composite(mapped_column("amount", Integer()), mapped_column("unit", String(40)))

    def __repr__(self) -> str:
        return f"<{self.id=} {self.weight=}>"


engine = create_engine("sqlite:///:memory:", echo=True)
MyBase.metadata.create_all(engine)

with engine.connect() as connection:
    session = Session(bind=connection)
    session.execute(insert(Weights).values(weight=Weight(10, "lbs")))
    result = session.execute(select(Weights))
    print(result.scalars().all())
