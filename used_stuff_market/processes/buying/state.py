from pydantic import BaseModel

from used_stuff_market.utils import Money


class BuyingProcessState(BaseModel):
    price: Money
    ...
