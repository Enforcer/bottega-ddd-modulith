.PHONY: fmt
fmt:
	uv run ruff format used_stuff_market/ tests/
.PHONY: test
test:
	uv run pytest tests/

.PHONY: lint
lint:
	uv run mypy used_stuff_market/ tests/
	uv run ruff check --fix used_stuff_market/ tests/

.PHONY: qa
qa: fmt lint test

.PHONY: run
run:
	uv run uvicorn used_stuff_market.api.app:app

.PHONY: run-reload
run-reload:
	uv run uvicorn used_stuff_market.api.app:app --reload

.PHONY: migrate
migrate:
	uv run alembic -c used_stuff_market/db/alembic.ini upgrade head

.PHONY: arch-test
arch-test:
	uv run lint-imports

# Use `uv run celery --app=used_stuff_market.workers.with_celery call used_stuff_market.catalog.tasks.catalog_task` to test
.PHONY: worker
worker:
	uv run celery --app=used_stuff_market.workers.with_celery worker -l INFO --pool threads --concurrency=2

.PHONY: worker-reload
worker-reload:
	uv run watchfiles "celery --app=used_stuff_market.workers.with_celery worker -l INFO --pool threads --concurrency=2" used_stuff_market/
