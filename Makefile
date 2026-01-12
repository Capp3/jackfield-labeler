# Jackfield Labeler - Lean Makefile
# Single source of truth for development commands

.PHONY: help install check test run build build-exe clean docs-check release lint fix dev black isort mypy pylint pyright pytest coverage radon profile bandit all

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := uv run python
PACKAGE := jackfield_labeler
DIST_DIR := dist
SITE_DIR := site
TEMP_DIR := $(shell echo $${TMPDIR:-/tmp})

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

lint: ## Run linting checks (ruff check)
	@echo "🔍 Running linting checks..."
	@uv run ruff check

fix: ## Auto-fix linting issues and format code
	@echo "🔧 Auto-fixing linting issues..."
	@uv run ruff check --fix
	@echo "✨ Formatting code..."
	@uv run ruff format

test: ## Run tests with coverage
	@echo "🧪 Running tests..."
	@QT_QPA_PLATFORM=offscreen xvfb-run -a uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml -v

run: ## Run the application
	@echo "🎯 Starting Jackfield Labeler..."
	@uv run -m $(PACKAGE)

build: clean ## Build wheel distribution
	@echo "📦 Building wheel..."
	@uvx --from build pyproject-build --installer uv

build-exe: ## Build executable (requires PyInstaller)
	@echo "🔨 Building executable..."
	@uv run pyinstaller jackfield_labeler.spec --noconfirm

clean: ## Clean build artifacts and virtual environment
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf $(DIST_DIR) build *.egg-info .pytest_cache .coverage .venv .ruff_cache .mypy_cache
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true

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

black: ## Format code with black
	@echo "🔧 Formatting code..."
	@uv run black jackfield_labeler/.

isort: ## Sort imports with isort
	@echo "🔧 Sorting imports..."
	@uv run isort jackfield_labeler/.

mypy: ## Run type checks with mypy
	@echo "🔍 Running type checks..."
	@uv run mypy jackfield_labeler/.

pylint: ## Run pylint checks
	@echo "🔍 Running pylint checks..."
	@uv run pylint jackfield_labeler/.

pyright: ## Run type checks with pyright
	@echo "🔍 Running pyright checks..."
	@uv run pyright jackfield_labeler/.

pytest: ## Run tests with pytest
	@echo "🧪 Running tests..."
	@uv run pytest --maxfail=1 --disable-warnings jackfield_labeler/.

coverage: ## Generate coverage report
	@echo "🔍 Running coverage checks..."
	@uv run coverage run -m pytest
	@uv run coverage report -m

radon: ## Analyze code complexity with radon
	@echo "🔍 Running radon checks..."
	@uv run radon cc -a jackfield_labeler/.

profile: ## Profile application performance
	@echo "🔍 Running profiling..."
	@$(PYTHON) -m cProfile jackfield_labeler/app.py
	@$(PYTHON) -m cProfile -o profile.prof jackfield_labeler/app.py
	@snakeviz profile.prof

bandit: ## Run security checks with bandit
	@echo "🔍 Running bandit checks..."
	@uv run bandit -r jackfield_labeler/.

all: clean install check test build ## Run full development cycle
	@echo "🎯 Full development cycle complete!"

# =============================================================================
# Cursor Memory Bank
# =============================================================================
# Source: https://github.com/vanzan01/cursor-memory-bank
# Provides AI-powered development commands and rules for Cursor IDE

update-memory-bank: ## Update the memory bank commands and rules
	@echo "Updating Cursor Memory Bank..."
	@mkdir -p $(TEMP_DIR)
	@if git clone --depth 1 https://github.com/vanzan01/cursor-memory-bank.git $(TEMP_DIR)/cursor-memory-bank 2>/dev/null; then \
		echo "Successfully cloned cursor-memory-bank repository"; \
		if [ -d "$(TEMP_DIR)/cursor-memory-bank/.cursor/commands" ]; then \
			mkdir -p .cursor/commands; \
			cp -R $(TEMP_DIR)/cursor-memory-bank/.cursor/commands/* .cursor/commands/ && \
			echo "Commands updated successfully"; \
		else \
			echo "Warning: Commands directory not found in repository"; \
		fi; \
		if [ -d "$(TEMP_DIR)/cursor-memory-bank/.cursor/rules/isolation_rules" ]; then \
			mkdir -p .cursor/rules/isolation_rules; \
			cp -R $(TEMP_DIR)/cursor-memory-bank/.cursor/rules/isolation_rules/* .cursor/rules/isolation_rules/ && \
			echo "Isolation rules updated successfully"; \
		else \
			echo "Warning: Isolation rules directory not found in repository"; \
		fi; \
		rm -rf $(TEMP_DIR)/cursor-memory-bank; \
		echo "Memory bank update complete."; \
	else \
		echo "Error: Failed to clone cursor-memory-bank repository"; \
		echo "Please check your internet connection and try again"; \
		exit 1; \
	fi

install-memory-bank: update-memory-bank ## Install the memory bank commands and rules (alias for update)

# =============================================================================
# Awesome Cursor Rules
# =============================================================================
# Source: https://github.com/PatrickJS/awesome-cursorrules
# Collection of cursor rules for various frameworks and languages

update-rules: ## Update cursor rules for frameworks and languages
	@echo "Updating Awesome Cursor Rules..."
	@mkdir -p $(TEMP_DIR)
	@if git clone https://github.com/PatrickJS/awesome-cursorrules.git $(TEMP_DIR)/awesome-cursorrules 2>/dev/null; then \
		echo "Successfully cloned awesome-cursorrules repository"; \
		echo "$$(date +%s)000" > /tmp/timestamp.txt; \
		TIMESTAMP=$$(cat /tmp/timestamp.txt); \
		echo "{\"id\":\"log_$$TIMESTAMP_1\",\"timestamp\":$$TIMESTAMP,\"location\":\"Makefile:177\",\"message\":\"Repository cloned\",\"data\":{\"repo_path\":\"$(TEMP_DIR)/awesome-cursorrules\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"A\"}" >> /Users/dcapp3/code/jackfield-labeler/.cursor/debug.log; \
		echo "{\"id\":\"log_$$TIMESTAMP_2\",\"timestamp\":$$TIMESTAMP,\"location\":\"Makefile:179\",\"message\":\"Root directory listing\",\"data\":{\"root_files\":\"$$(ls -la $(TEMP_DIR)/awesome-cursorrules | head -20 | tr '\n' ' ')\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"A\"}" >> /Users/dcapp3/code/jackfield-labeler/.cursor/debug.log; \
		echo "{\"id\":\"log_$$TIMESTAMP_3\",\"timestamp\":$$TIMESTAMP,\"location\":\"Makefile:179\",\"message\":\"Checking .cursor/rules\",\"data\":{\"exists\":\"$$([ -d '$(TEMP_DIR)/awesome-cursorrules/.cursor/rules' ] && echo 'true' || echo 'false')\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"A\"}" >> /Users/dcapp3/code/jackfield-labeler/.cursor/debug.log; \
		echo "{\"id\":\"log_$$TIMESTAMP_4\",\"timestamp\":$$TIMESTAMP,\"location\":\"Makefile:179\",\"message\":\"Checking .cursorrules\",\"data\":{\"exists\":\"$$([ -d '$(TEMP_DIR)/awesome-cursorrules/.cursorrules' ] && echo 'true' || echo 'false')\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"B\"}" >> /Users/dcapp3/code/jackfield-labeler/.cursor/debug.log; \
		echo "{\"id\":\"log_$$TIMESTAMP_5\",\"timestamp\":$$TIMESTAMP,\"location\":\"Makefile:179\",\"message\":\"Checking rules directory\",\"data\":{\"exists\":\"$$([ -d '$(TEMP_DIR)/awesome-cursorrules/rules' ] && echo 'true' || echo 'false')\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"B\"}" >> /Users/dcapp3/code/jackfield-labeler/.cursor/debug.log; \
		echo "{\"id\":\"log_$$TIMESTAMP_6\",\"timestamp\":$$TIMESTAMP,\"location\":\"Makefile:179\",\"message\":\"All directories with cursor/rules\",\"data\":{\"find_results\":\"$$(find $(TEMP_DIR)/awesome-cursorrules -type d -name '*cursor*' -o -type d -name '*rules*' 2>/dev/null | head -10 | tr '\n' ' ')\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"C\"}" >> /Users/dcapp3/code/jackfield-labeler/.cursor/debug.log; \
		if [ -d "$(TEMP_DIR)/awesome-cursorrules/rules-new" ]; then \
			echo "{\"id\":\"log_$$TIMESTAMP_7\",\"timestamp\":$$TIMESTAMP,\"location\":\"Makefile:187\",\"message\":\"Copying from rules directory\",\"data\":{\"source\":\"$(TEMP_DIR)/awesome-cursorrules/rules-new\",\"dest\":\".cursor/rules\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"D\"}" >> /Users/dcapp3/code/jackfield-labeler/.cursor/debug.log; \
			mkdir -p .cursor/rules; \
			cp -R $(TEMP_DIR)/awesome-cursorrules/rules-new/* .cursor/rules/ && \
			echo "Rules updated successfully"; \
		else \
			echo "{\"id\":\"log_$$TIMESTAMP_8\",\"timestamp\":$$TIMESTAMP,\"location\":\"Makefile:191\",\"message\":\"Rules directory not found\",\"data\":{\"checked_path\":\"$(TEMP_DIR)/awesome-cursorrules/rules\"},\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"D\"}" >> /Users/dcapp3/code/jackfield-labeler/.cursor/debug.log; \
			echo "Warning: Rules directory not found in repository"; \
		fi; \
		rm -rf $(TEMP_DIR)/awesome-cursorrules; \
		echo "Rules update complete."; \
	else \
		echo "Error: Failed to clone awesome-cursorrules repository"; \
		echo "Please check your internet connection and try again"; \
		exit 1; \
	fi

install-rules: update-rules ## Install cursor rules (alias for update)

# =============================================================================
# Combined Installation
# =============================================================================

vibe: install-rules install-memory-bank ## Install both cursor rules and memory bank
	@echo ""
	@echo "=========================================="
	@echo "Vibe setup complete!"
	@echo "=========================================="
	@echo "Installed:"
	@echo "  - Cursor Memory Bank (commands & rules)"
	@echo "  - Awesome Cursor Rules (framework rules)"
	@echo ""
	@echo "Please restart Cursor IDE to load the new configurations."
	@echo ""
