.PHONY: help install format lint test security typecheck run ci clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Create venv and install all dependencies
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(VENV)/bin/pre-commit install
	@echo "\n✅  Environment ready. Activate with: source $(VENV)/bin/activate"

format: ## Auto-format code (Black + isort)
	$(VENV)/bin/black .
	$(VENV)/bin/isort .

lint: ## Run all linters (Ruff, Black check, isort check)
	$(VENV)/bin/ruff check .
	$(VENV)/bin/black --check --diff .
	$(VENV)/bin/isort --check-only --diff .

test: ## Run tests with coverage
	$(VENV)/bin/pytest -v --tb=short --cov=src --cov-report=term-missing --cov-fail-under=80

security: ## Run security scans (Bandit + detect-secrets)
	$(VENV)/bin/bandit -r src/ -c pyproject.toml
	$(VENV)/bin/detect-secrets scan --baseline .secrets.baseline

typecheck: ## Run mypy type checking
	$(VENV)/bin/mypy src/

run: ## Start the Streamlit application
	$(VENV)/bin/streamlit run app.py

ci: lint security test typecheck ## Run full CI pipeline locally
	@echo "\n✅  All CI checks passed!"

clean: ## Remove generated files and caches
	rm -rf $(VENV) .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "🧹  Cleaned."
