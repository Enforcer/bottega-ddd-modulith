"""Goal of the `main` component is to assemble the application.

Typically, this means reading settings and initializing dependency injection container.

This is reusable part between different ways to run the application - whether it is HTTP server with FastAPI or worker pool on top of Celery.
"""
