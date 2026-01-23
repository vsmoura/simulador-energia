.PHONY: install run migrate seed test

install:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

migrate:
	python -m app.infrastructure.db.cli migrate

seed:
	python -m app.infrastructure.db.cli seed

run:
	uvicorn app.main:app --reload --port 8000

test:
	pytest
