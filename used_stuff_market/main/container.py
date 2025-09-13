from lagom import Container
from lagom.integrations.fast_api import FastApiIntegration

container = Container()
deps = FastApiIntegration(container)
# Documentation: https://lagom-di.readthedocs.io/en/latest/framework_integrations/#fastapi
