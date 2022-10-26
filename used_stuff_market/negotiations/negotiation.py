from uuid import UUID

from used_stuff_market.shared_kernel.money import Money


class NegotiationClosed(Exception):
    pass


class Negotiation:
    def __init__(self, offer: Money, offerer: UUID, offeree: UUID) -> None:
        """
        :param offer: how much was originally offered?
        :param oferrer: who offered that price?
        :param oferee: who is this price offered to?
        """
        pass

    @property
    def offer(self) -> Money:
        pass

    def accept_offer(self, party: UUID) -> None:
        pass

    def reject_offer(self, party: UUID) -> None:
        pass

    def propose_counter_offer(self, party: UUID, counter_offer: Money) -> None:
        pass
