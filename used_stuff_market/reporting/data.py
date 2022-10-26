from random import choice
from typing import Iterator

from used_stuff_market.shared_kernel.money import Currency, Money


def fetch() -> Iterator[tuple]:
    random_id = choice(range(10_000))
    ids = iter(range(random_id, random_id + 10))
    for item_id in ids:
        yield (
            item_id,
            Money(
                Currency.from_code("USD"),
                choice(["10.99", "12.99", "13.99", "99.00", "500"]),
            ),
            Money(Currency.from_code("USD"), choice(["1.99", "2.49", "3.15", "4.20"])),
        )
