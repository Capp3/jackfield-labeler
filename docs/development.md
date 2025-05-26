# Development Guide

## Environment Setup

### Prerequisites

- Python 3.12+
- UV package manager

### Setting Up Your Development Environment

```bash
# Clone the repository
git clone https://github.com/capp3/jackfield-labeler.git
cd jackfield-labeler

# Create and activate virtual environment using UV
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .
uv pip install -e ".[dev]"
```

## Running the Application

```bash
# Run directly with UV
uv run -m jackfield_labeler

# Alternatively, after installing in development mode
python -m jackfield_labeler
```

## Managing Dependencies

### Adding Dependencies

```bash
# Add a production dependency
uv add package_name

# Add a development dependency
uv add --dev package_name
```

### Updating Dependencies

```bash
# Update all dependencies
uv pip compile --upgrade

# Update a specific dependency
uv add --upgrade package_name
```

## Development Workflow

1. Create a feature branch
2. Make your changes
3. Run tests: `uv run pytest`
4. Run linting: `uv run ruff check .`
5. Run formatting: `uv run ruff format .`
6. Submit a pull request

## Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality:

```bash
uv run pre-commit install
```

This will install the hooks specified in `.pre-commit-config.yaml`.
