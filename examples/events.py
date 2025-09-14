from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Type, Any, Callable


class EventBus:
    def __init__(self) -> None:
        self._subscriptions: dict[Type[Any], list[Callable[[Any], None]]] = defaultdict(
            list
        )

    def subscribe(self, event: Type[Any], subscriber: Callable[[Any], None]) -> None:
        self._subscriptions[event].append(subscriber)

    def publish(self, event: Any) -> None:
        for subscriber in self._subscriptions[type(event)]:
            subscriber(event)


@dataclass(frozen=True)
class SprintStarted:
    id: int
    name: str
    when: datetime


def sprint_started_handler(sprint_started: SprintStarted) -> None:
    print("Got event!", sprint_started)


some_event_bus = EventBus()  # just once is enough
some_event_bus.subscribe(SprintStarted, sprint_started_handler)

some_event_bus.publish(
    SprintStarted(id=1, name="Sprint UsedStuffMarket #1", when=datetime(2022, 9, 4, 8)),
)
