from fastapi import Depends, FastAPI

from used_stuff_market.api import catalog, items, likes, negotations, orders
from used_stuff_market.api.session_deps import get_session

app = FastAPI(dependencies=[Depends(get_session)])
app.include_router(items.router)
app.include_router(negotations.router)
app.include_router(catalog.router)
app.include_router(orders.router)
app.include_router(likes.router)
