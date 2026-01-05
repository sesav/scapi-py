VIRTUAL_ENV ?= .venv
PYTHON_VERSION ?= 3.10
PYTHON_VERSION_FILE ?= .python-version
SHELL := /bin/bash

.PHONY: all

.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  reinstall  - Reinstall dependencies"
	@echo "  run        - Run scapi app"
	@echo "  lint       - Run code linting"
	@echo "  format     - Format code"
	@echo "  test       - Run tests"
	@echo "  clean      - Clean temporary files"

$(VIRTUAL_ENV):
	uv venv

$(PYTHON_VERSION_FILE): | $(VIRTUAL_ENV)
	uv python install $(PYTHON_VERSION)
	uv python pin $(PYTHON_VERSION)

.deps: pyproject.toml $(PYTHON_VERSION_FILE)
	uv sync --all-extras --dev
	uv tool install pre-commit
	uv run pre-commit install
	uv run pre-commit install-hooks
	@touch .deps

install: .deps
	@printf "\nSetup complete! To activate the virtual environment, run:\n\n    source $(VIRTUAL_ENV)/bin/activate\n"

reinstall: clean install

run:
	uv run scapi.py

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	rm -r coverage; \
	uv run coverage run --source=. -m pytest -v -p no:warnings .; \
	uv run coverage combine; \
	uv run coverage report --fail-under=100

clean:
	rm -rf .venv .pytest_cache .ruff_cache .coverage coverage dist *.egg-info .deps .python-version uv.lock
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
