# Jackfield Labeler - Lean Makefile
# Single source of truth for development commands

.PHONY: help install check test run build clean docs release

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := uv run python
PACKAGE := jackfield_labeler
DIST_DIR := dist
SITE_DIR := site

help: ## Show this help message
	@echo "🚀 Jackfield Labeler - Development Commands"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies and pre-commit hooks
	@echo "📦 Installing dependencies..."
	@uv sync
	@echo "🔧 Installing pre-commit hooks..."
	@uv run pre-commit install

check: ## Run all quality checks (linting, formatting, type checking)
	@echo "🔍 Running quality checks..."
	@uv lock --locked
	@uv run pre-commit run -a

test: ## Run tests with coverage
	@echo "🧪 Running tests..."
	@QT_QPA_PLATFORM=offscreen xvfb-run -a uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml -v

test-watch: ## Run tests in watch mode
	@echo "👀 Running tests in watch mode..."
	@QT_QPA_PLATFORM=offscreen xvfb-run -a uv run python -m pytest --cov --cov-config=pyproject.toml -f

run: ## Run the application
	@echo "🎯 Starting Jackfield Labeler..."
	@uv run -m $(PACKAGE)

build: clean ## Build wheel distribution
	@echo "📦 Building wheel..."
	@uvx --from build pyproject-build --installer uv

build-exe: ## Build executable (requires PyInstaller)
	@echo "🔨 Building executable..."
	@uv run pyinstaller jackfield_labeler.spec --noconfirm

clean: ## Clean build artifacts
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf $(DIST_DIR) build *.egg-info .pytest_cache .coverage
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true

docs-build: ## Build documentation
	@echo "📚 Building documentation..."
	@uv run mkdocs build

docs-serve: ## Serve documentation locally
	@echo "🌐 Serving documentation at http://127.0.0.1:8000"
	@uv run mkdocs serve

docs-check: ## Check documentation build
	@echo "✅ Checking documentation..."
	@uv run mkdocs build -s

release: ## Create a new release (usage: make release VERSION=1.0.0)
	@if [ -z "$(VERSION)" ]; then \
		echo "❌ Error: VERSION is required. Usage: make release VERSION=1.0.0"; \
		exit 1; \
	fi
	@echo "🚀 Creating release $(VERSION)..."
	@git checkout main
	@git pull
	@sed -i "s/version = \".*\"/version = \"$(VERSION)\"/" pyproject.toml
	@git add pyproject.toml
	@git commit -m "Bump version to $(VERSION)"
	@git tag -a "v$(VERSION)" -m "Release version $(VERSION)"
	@git push origin main
	@git push origin "v$(VERSION)"
	@echo "✅ Release $(VERSION) created and pushed!"

dev: install ## Set up development environment
	@echo "🎉 Development environment ready!"

ci: check test docs-check ## Run CI checks locally
	@echo "✅ All CI checks passed!"

all: clean install ci build ## Run full development cycle
	@echo "🎯 Full development cycle complete!"
