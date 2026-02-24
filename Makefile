venv:
	python -m venv .venv

install:
	pip install -r requirements.txt

run:
	python -m src.pipeline.run_all

lint:
	ruff check .

test:
	pytest -q
