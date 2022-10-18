.PHONY: fmt
fmt:
	isort used_stuff_market/
	black used_stuff_market/

.PHONY: test
test:
	pytest tests


.PHONY: run
run:
	uvicorn used_stuff_market.api.app:app

.PHONY: run-reload
run-reload:
	uvicorn used_stuff_market.api.app:app --reload

.PHONY: run-celery-reload
run-celery-reload:
	watchfiles "celery -A used_stuff_market.workers.with_celery worker --loglevel=INFO" used_stuff_market/

