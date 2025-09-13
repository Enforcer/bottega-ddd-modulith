from typing import Iterator

from lagom import Container, context_dependency_definition, ContextContainer
from lagom.integrations.fast_api import FastApiIntegration
from sqlalchemy.orm import Session

from used_stuff_market.db import db_session

container = Container()
deps = FastApiIntegration(container, request_context_singletons=[Session])
# Documentation: https://lagom-di.readthedocs.io/en/latest/framework_integrations/#fastapi
context_container = ContextContainer(container, context_types=[Session])


@context_dependency_definition(container)  # type: ignore
def request_scoped_session() -> Iterator[Session]:
    with db_session() as session:
        yield session
