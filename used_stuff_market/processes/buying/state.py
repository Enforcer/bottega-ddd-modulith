from pydantic import BaseModel

from used_stuff_market.shared_kernel.money import Money


class BuyingProcessState(BaseModel):
    price: Money
    ...
