.PHONY: install test lint format clean build publish-test

install:
	poetry install

test:
	poetry run pytest

lint:
	poetry run flake8 pubmed_fetcher tests
	poetry run mypy pubmed_fetcher

format:
	poetry run black pubmed_fetcher tests
	poetry run isort pubmed_fetcher tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

build:
	poetry build

publish-test:
	poetry publish -r testpypi

all: install lint test format 