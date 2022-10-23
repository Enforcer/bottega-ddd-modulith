from lagom.integrations.fast_api import FastApiIntegration

from used_stuff_market.main import container

__all__ = ["Injects"]

integration = FastApiIntegration(container)
Injects = integration.depends
