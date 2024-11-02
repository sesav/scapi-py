.PHONY: all

SHELL := /bin/bash

.DEFAULT_GOAL := lint

install:
	uv python install 3.12
	uv python pin 3.12
	uv sync --all-extras --dev
	uv run pre-commit install && uv run pre-commit install-hooks

lint:
	uv run pre-commit run --all-files

ruff:
	uv run ruff check --config ruff.toml

test:
	rm -r coverage; \
	uv run coverage run --source=. -m pytest -v -p no:warnings .; \
	uv run coverage combine; \
	uv run coverage report --fail-under=85
