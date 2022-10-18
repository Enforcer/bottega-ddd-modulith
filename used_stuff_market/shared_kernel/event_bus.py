from collections import defaultdict
from typing import Any, Callable, Type


class EventBus:
    def __init__(self) -> None:
        self._subscriptions: dict[Type, list[Callable]] = defaultdict(list)

    def subscribe(self, event: Type, subscriber: Callable) -> None:
        self._subscriptions[event].append(subscriber)

    def publish(self, event: Any) -> None:
        for subscriber in self._subscriptions[type(event)]:
            subscriber(event)


event_bus = EventBus()
