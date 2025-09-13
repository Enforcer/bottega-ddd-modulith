from fastapi import FastAPI

from used_stuff_market.api import catalog, items, likes, negotations, orders, users

app = FastAPI()
app.include_router(items.router)
app.include_router(negotations.router)
app.include_router(catalog.router)
app.include_router(orders.router)
app.include_router(likes.router)
app.include_router(users.router)
