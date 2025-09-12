# Set the default target to 'help'
.DEFAULT_GOAL := help

.PHONY: help install format lint clean clean-pyc clean-pytestcache makemigrations migrate reset-db test coverage runserver generate-data superuser check

# --- Project Check ---
check: migrate
	@echo "Running linter (flake8)..."
	pipenv run flake8 server/ --exclude=migrations
	@echo "Running tests with coverage (must be >90%)..."
	COVERAGE_FILE=server/.coverage pipenv run coverage run --rcfile=server/.coveragerc -m server.manage test
	COVERAGE_FILE=server/.coverage pipenv run coverage report --rcfile=server/.coveragerc --fail-under=90
	@echo "Generating synthetic data..."
	PYTHONPATH=$(CURDIR) pipenv run python3 -m server.manage load_demo_data

# --- General/Utility Targets ---
help:
	@echo "Available targets:"
	@awk -F: '/^[a-zA-Z0-9_-]+:/ {print $$1}' Makefile | sort | uniq

install:
	pipenv install --dev

# --- Code Quality ---
format: install
	pipenv run black server/

lint: install format
	pipenv run flake8 server/ --exclude=migrations

# --- Cleaning ---
clean: clean-pyc clean-pytestcache
	rm -rf htmlcov .coverage

clean-pyc:
	find . -type d -name '__pycache__' -exec rm -rf {} +

clean-pytestcache:
	rm -rf .pytest_cache

# --- Database & Migrations ---
makemigrations: install
	PYTHONPATH=$(CURDIR) pipenv run python3 -m server.manage makemigrations

migrate: install makemigrations
	PYTHONPATH=$(CURDIR) pipenv run python3 -m server.manage migrate

reset-db: install clean-pyc clean-pytestcache
	rm -f server/db.sqlite3
	$(MAKE) migrate

# --- Testing ---
test: install clean-pyc clean-pytestcache
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(CURDIR) pipenv run python3 -m server.manage test --parallel

coverage: install clean-pyc clean-pytestcache
	COVERAGE_FILE=server/.coverage pipenv run coverage run --rcfile=server/.coveragerc -m server.manage test
	COVERAGE_FILE=server/.coverage pipenv run coverage report --rcfile=server/.coveragerc
	COVERAGE_FILE=server/.coverage pipenv run coverage html --rcfile=server/.coveragerc
