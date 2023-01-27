from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class NegotiationId:
    item_id: int
    offerer: UUID
    offeree: UUID
