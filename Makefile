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

