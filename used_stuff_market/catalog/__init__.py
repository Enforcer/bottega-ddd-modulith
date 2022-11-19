from used_stuff_market.catalog import tasks
from used_stuff_market.catalog.facade import Catalog
from used_stuff_market.likes.events import ItemLiked, ItemUnliked
from used_stuff_market.shared_kernel.event_bus import event_bus


__all__ = ["Catalog"]


def item_liked_handler(event: ItemLiked) -> None:
    tasks.increase_likes.delay(item_id=event.item_id)


def item_unliked_handler(event: ItemUnliked) -> None:
    tasks.decrease_likes.delay(item_id=event.item_id)


event_bus.subscribe(ItemLiked, item_liked_handler)
event_bus.subscribe(ItemUnliked, item_unliked_handler)
