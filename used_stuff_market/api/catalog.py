from fastapi.routing import APIRouter

from used_stuff_market.catalog import Catalog
from used_stuff_market.main.container import deps

router = APIRouter()


@router.get("/catalog/search/{term}")
def search(term: str, catalog: Catalog = deps.depends(Catalog)) -> list[dict]:
    return catalog.search(term)
