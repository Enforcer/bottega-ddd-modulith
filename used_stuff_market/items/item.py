from uuid import UUID

import attr

from used_stuff_market.utils import Money


@attr.s(auto_attribs=True)
class Item:
    id: int = attr.ib(init=False)
    owner_id: UUID
    title: str
    description: str
    starting_price: Money
