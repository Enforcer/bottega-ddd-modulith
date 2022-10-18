from fastapi.routing import APIRouter

from used_stuff_market.catalog import Catalog

router = APIRouter()


@router.get("/catalog/search/{term}")
def search(term: str) -> list[dict]:
    catalog = Catalog()
    return catalog.search(term)
