from uuid import UUID

from used_stuff_market.shared_kernel.money import Money


class Item:
    id: int
    owner_id: UUID
    title: str
    description: str
    starting_price: Money

    def __init__(
        self, owner_id: UUID, title: str, description: str, starting_price: Money
    ) -> None:
        self.owner_id = owner_id
        self.title = title
        self.description = description
        self.starting_price = starting_price
