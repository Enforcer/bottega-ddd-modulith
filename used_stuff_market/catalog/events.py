from attr import define


@define(frozen=True)
class ItemLiked:
    item_id: int


@define(frozen=True)
class ItemUnliked:
    item_id: int
