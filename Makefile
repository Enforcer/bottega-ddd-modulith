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

.PHONY: run-celery-reload
run-celery-reload:
	uv run watchfiles "celery -A used_stuff_market.workers.with_celery worker --loglevel=INFO" used_stuff_market/

