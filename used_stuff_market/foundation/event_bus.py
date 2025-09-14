from lagom import Container
from collections import defaultdict
from typing import Any, Callable, Type, ContextManager, Protocol


class EventHandler(Protocol):
    def __call__(self, event: Any, *args: Any) -> None: ...


class EventBus:
    def __init__(
        self,
        container: Container,
        context_maker: Callable[[Container], ContextManager[Container]],
    ) -> None:
        self._container = container
        self._context_maker = context_maker
        self._subscriptions: dict[Type[Any], list[EventHandler]] = defaultdict(list)

    def subscribe(self, event: Type[Any], subscriber: EventHandler) -> None:
        self._subscriptions[event].append(subscriber)

    def publish(self, event: Any) -> None:
        for subscriber in self._subscriptions[type(event)]:
            with self._context_maker(self._container) as container:
                bound_event_handler = container.magic_partial(
                    subscriber, keys_to_skip=["event"]
                )
                bound_event_handler(event)
