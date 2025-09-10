from dataclasses import dataclass
from datetime import datetime

from used_stuff_market.utils import EventBus


@dataclass(frozen=True)
class SprintStarted:
    id: int
    name: str
    when: datetime


def sprint_started_handler(sprint_started: SprintStarted) -> None:
    print("Got event!", sprint_started)


event_bus = EventBus()  # just once is enough
event_bus.subscribe(SprintStarted, sprint_started_handler)

event_bus.publish(
    SprintStarted(id=1, name="Sprint UsedStuffMarket #1", when=datetime(2022, 9, 4, 8)),
)
