from contextlib import contextmanager
from typing import ContextManager, Iterator

from lagom import (
    Container,
    context_dependency_definition,
    ContextContainer,
    UnresolvableTypeDefinition,
)
from lagom.integrations.fast_api import FastApiIntegration
from sqlalchemy.orm import Session

from used_stuff_market.db import session_factory

container = Container()
container[Session] = UnresolvableTypeDefinition(
    "Use ContextManager[Session] to get Session instance."
)

deps = FastApiIntegration(container, request_context_singletons=[Session])
# Documentation: https://lagom-di.readthedocs.io/en/latest/framework_integrations/#fastapi
context_container = ContextContainer(container, context_types=[Session])


@context_dependency_definition(container)  # type: ignore
def session_with_cleanup() -> Iterator[Session]:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def manage_session(a_container: Container) -> Iterator[Container]:
    """This context manager ensures there is a Session instance in the container.

    First, it ensures that always the same session will be returned (.temporary_singletons).
    Then, it initiates session using ContextManager[Session].
    Finally, a container is cloned to be reconfigured for returning the constructed Session.
    """
    with a_container.temporary_singletons(singletons=[Session]):
        with a_container[ContextManager[Session]] as _session:  # type: ignore
            container_with_session = a_container.clone()
            container_with_session[Session] = _session
            yield container_with_session
