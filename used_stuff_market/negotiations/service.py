from uuid import UUID

from used_stuff_market.availability import Availability
from used_stuff_market.negotiations.negotiation import Negotiation
from used_stuff_market.negotiations.negotiation_id import NegotiationId
from used_stuff_market.negotiations.repository import NegotiationsRepository
from used_stuff_market.shared_kernel.money import Money


class Negotiations:
    def __init__(
        self, availability: Availability, repository: NegotiationsRepository
    ) -> None:
        self._availability = availability
        self._repository = repository

    def start(
        self, item_id: int, owner: UUID, offerer: UUID, offeree: UUID, offer: Money
    ) -> None:
        negotiation = Negotiation(
            item_id=item_id, owner=owner, offerer=offerer, offeree=offeree, offer=offer
        )
        self._repository.add(negotiation)

    def accept(self, negotiation_id: NegotiationId, party: UUID) -> None:
        negotiation = self._repository.get(negotiation_id)
        negotiation.accept_offer(party=party)
        self._availability.lock_resource(  # type: ignore
            resource_id=negotiation_id.item_id, lock_for=negotiation_id.offerer
        )
