from used_stuff_market.negotiations.negotiation import Negotiation
from used_stuff_market.negotiations.negotiation_id import NegotiationId


class NegotiationsRepository:
    def __init__(self) -> None:
        self._negotiations: dict[NegotiationId, Negotiation] = {}

    def add(self, negotiation: Negotiation) -> None:
        self._negotiations[negotiation.id] = negotiation

    def get(self, negotiation_id: NegotiationId) -> Negotiation:
        return self._negotiations[negotiation_id]
