.PHONY: fmt
fmt:
	isort used_stuff_market/ tests/
	black used_stuff_market/ tests/

.PHONY: test
test:
	pytest tests/

.PHONY: lint
lint:
	mypy used_stuff_market/ tests/
	flake8 used_stuff_market/ tests/

.PHONY: qa
qa: lint test

.PHONY: run
run:
	uvicorn used_stuff_market.api.app:app

.PHONY: run-reload
run-reload:
	uvicorn used_stuff_market.api.app:app --reload

.PHONY: run-celery-reload
run-celery-reload:
	watchfiles "celery -A used_stuff_market.workers.with_celery worker --loglevel=INFO" used_stuff_market/

