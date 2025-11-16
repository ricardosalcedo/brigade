# BRIGADE Makefile

.PHONY: test install-test clean lint format type-check security help

help:
	@echo "🎖️ BRIGADE Development Commands"
	@echo "================================"
	@echo "test          - Run all tests"
	@echo "install-test  - Install test dependencies"
	@echo "lint          - Run code linting"
	@echo "format        - Format code"
	@echo "type-check    - Run type checking"
	@echo "security      - Run security checks"
	@echo "clean         - Clean up test artifacts"

install-test:
	pip install -r requirements-test.txt

test:
	python run_tests.py

test-unit:
	python -m pytest tests/unit/ -v

test-integration:
	python -m pytest tests/integration/ -v

test-coverage:
	python -m pytest tests/ --cov=core --cov=analyzers --cov=workflows --cov-report=html

lint:
	flake8 core/ analyzers/ workflows/ --max-line-length=100

format:
	black core/ analyzers/ workflows/
	isort core/ analyzers/ workflows/

format-check:
	black --check core/ analyzers/ workflows/
	isort --check-only core/ analyzers/ workflows/

type-check:
	mypy core/ analyzers/ workflows/ --ignore-missing-imports

security:
	bandit -r core/ analyzers/ workflows/
	safety check

clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf *.json
	rm -rf *_report.md
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Pre-commit simulation
pre-commit: format-check lint test-unit
	@echo "✅ Pre-commit checks passed"

# CI simulation  
ci: install-test test lint security type-check
	@echo "✅ CI pipeline completed"
