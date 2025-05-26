# Development Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Environment](#development-environment)
3. [Project Structure](#project-structure)
4. [Coding Standards](#coding-standards)
5. [Testing](#testing)
6. [Documentation](#documentation)
7. [Git Workflow](#git-workflow)
8. [Release Process](#release-process)
9. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

Before you begin development, ensure you have:

- **Python 3.12+** installed
- **Git** for version control
- **UV** package manager (recommended over pip)
- A code editor with Python support (VS Code, PyCharm, etc.)

### Initial Setup

1. **Fork and Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/jackfield-labeler.git
   cd jackfield-labeler
   ```

2. **Install UV (if not already installed)**

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # or on Windows:
   # powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Set Up Development Environment**

   ```bash
   make install
   # or manually:
   uv sync
   uv run pre-commit install
   ```

4. **Verify Installation**

   ```bash
   make test
   make run
   ```

## Development Environment

### UV Package Manager

This project uses UV instead of pip for several advantages:

**Benefits:**

- Significantly faster dependency resolution and installation
- Built-in virtual environment management
- Better dependency conflict resolution
- Modern approach to Python packaging

**Common Commands:**

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add package-name

# Add a development dependency
uv add --group dev package-name

# Run the application
uv run -m jackfield_labeler

# Run tests
uv run pytest

# Run linting
uv run ruff check

# Format code
uv run ruff format
```

### Development Dependencies

The project includes several development tools:

```toml
[dependency-groups]
dev = [
    "pytest>=8.3.5",           # Testing framework
    "pytest-cov>=6.0.0",       # Coverage reporting
    "mypy>=1.15",               # Static type checking
    "ruff>=0.11.11",            # Linting and formatting
    "pre-commit>=4.0.1",        # Git hooks
    "mkdocs>=1.6.1",            # Documentation
    "mkdocs-material>=9.5.47",  # Documentation theme
]
```

### IDE Configuration

#### VS Code

Recommended extensions:

- Python
- Pylance
- Ruff
- GitLens

Settings (`.vscode/settings.json`):

```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "ruff",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"]
}
```

#### PyCharm

1. Set Python interpreter to the UV virtual environment
2. Enable Ruff for linting and formatting
3. Configure pytest as the test runner
4. Enable type checking with mypy

## Project Structure

### Directory Layout

```
jackfield-labeler/
├── .github/                 # GitHub workflows and templates
├── .vscode/                 # VS Code configuration
├── docs/                    # Documentation
├── examples/                # Sample projects and examples
├── jackfield_labeler/       # Main application package
│   ├── models/              # Data models
│   ├── views/               # UI components
│   ├── utils/               # Utility modules
│   └── controllers/         # Application logic
├── tests/                   # Test suite
├── .gitignore              # Git ignore rules
├── .pre-commit-config.yaml # Pre-commit hooks
├── Makefile                # Development commands
├── pyproject.toml          # Project configuration
├── README.md               # Project overview
└── uv.lock                 # Dependency lock file
```

### Module Organization

#### Models (`jackfield_labeler/models/`)

- **Purpose**: Data structures and business logic
- **Guidelines**:
  - Keep models UI-independent
  - Use dataclasses for simple data structures
  - Implement validation in `__post_init__`
  - Emit signals for UI updates

#### Views (`jackfield_labeler/views/`)

- **Purpose**: PyQt6 user interface components
- **Guidelines**:
  - Separate UI logic from business logic
  - Use signals for communication
  - Keep widgets focused and reusable
  - Follow Qt naming conventions

#### Utils (`jackfield_labeler/utils/`)

- **Purpose**: Utility functions and classes
- **Guidelines**:
  - Make utilities stateless when possible
  - Provide clear error handling
  - Document complex algorithms
  - Keep dependencies minimal

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications enforced by Ruff:

```toml
[tool.ruff]
target-version = "py312"
line-length = 120
fix = true

[tool.ruff.lint]
select = [
    "E", "W",    # pycodestyle
    "F",         # pyflakes
    "I",         # isort
    "B",         # flake8-bugbear
    "C4",        # flake8-comprehensions
    "UP",        # pyupgrade
    "RUF",       # ruff-specific rules
]
```

### Type Hints

All code must include type hints:

```python
# Good
def calculate_width(segments: List[Segment]) -> float:
    """Calculate total width of segments."""
    return sum(segment.width for segment in segments)

# Bad
def calculate_width(segments):
    return sum(segment.width for segment in segments)
```

### Documentation

#### Docstring Format

Use Google-style docstrings:

```python
def generate_pdf(self, label_strip: LabelStrip, filename: str, 
                rotation_angle: float | None = None) -> bool:
    """
    Generate PDF file from label strip.
    
    Args:
        label_strip: The label strip to render
        filename: Output PDF filename
        rotation_angle: Optional rotation override
        
    Returns:
        True if PDF was generated successfully, False otherwise
        
    Raises:
        RenderingError: If PDF generation fails
        FileNotFoundError: If output directory doesn't exist
    """
```

#### Code Comments

- Use comments sparingly for complex logic
- Prefer self-documenting code
- Explain "why" not "what"

```python
# Good
# Use center-to-center positioning to ensure consistent spacing
x_offset = (paper_width - total_width) / 2

# Bad
# Set x_offset to half the difference
x_offset = (paper_width - total_width) / 2
```

### Error Handling

#### Exception Hierarchy

```python
class JackfieldLabelerError(Exception):
    """Base exception for all application errors."""

class ValidationError(JackfieldLabelerError):
    """Raised when data validation fails."""

class FileFormatError(JackfieldLabelerError):
    """Raised when file format is invalid."""
```

#### Error Handling Patterns

```python
# Specific exception handling
try:
    strip = ProjectManager.load_project(filename)
except FileNotFoundError:
    logger.error(f"Project file not found: {filename}")
    return None
except FileFormatError as e:
    logger.error(f"Invalid project file format: {e}")
    return None

# Resource cleanup
try:
    with open(filename, 'w') as f:
        json.dump(data, f)
except IOError as e:
    logger.error(f"Failed to save project: {e}")
    raise
```

## Testing

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── test_models/             # Model tests
│   ├── test_label_strip.py
│   ├── test_segments.py
│   └── test_settings.py
├── test_utils/              # Utility tests
│   ├── test_pdf_generator.py
│   ├── test_strip_renderer.py
│   └── test_project_manager.py
└── test_integration/        # Integration tests
    ├── test_file_operations.py
    └── test_export_workflow.py
```

### Writing Tests

#### Unit Tests

```python
import pytest
from jackfield_labeler.models import LabelStrip, ContentSegment

class TestLabelStrip:
    def test_total_width_calculation(self):
        """Test that total width is calculated correctly."""
        strip = LabelStrip(content_cell_width=10.0)
        strip.add_content_segment("CH1")
        strip.add_content_segment("CH2")
        
        assert strip.get_total_width() == 20.0
    
    def test_segment_addition(self):
        """Test adding segments to strip."""
        strip = LabelStrip()
        initial_count = len(strip.segments)
        
        segment = strip.add_content_segment("Test")
        
        assert len(strip.segments) == initial_count + 1
        assert segment.text == "Test"
    
    @pytest.mark.parametrize("height,expected", [
        (5.0, 5.0),
        (10.5, 10.5),
        (0.1, 0.1),
    ])
    def test_height_values(self, height, expected):
        """Test various height values."""
        strip = LabelStrip(height=height)
        assert strip.height == expected
```

#### Integration Tests

```python
def test_pdf_generation_workflow():
    """Test complete PDF generation workflow."""
    # Create test strip
    strip = LabelStrip(height=6.0, content_cell_width=12.0)
    strip.add_content_segment("CH1", background_color="#FFFF00")
    strip.add_content_segment("CH2", background_color="#FF0000")
    
    # Generate PDF
    generator = PDFGenerator(strip.settings)
    output_file = "test_output.pdf"
    
    try:
        success = generator.generate_pdf(strip, output_file)
        assert success
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)
```

#### Fixtures

```python
# conftest.py
import pytest
from jackfield_labeler.models import LabelStrip, StripSettings

@pytest.fixture
def sample_strip():
    """Create a sample label strip for testing."""
    strip = LabelStrip(height=6.0, content_cell_width=12.0)
    strip.add_content_segment("CH1", background_color="#FFFF00")
    strip.add_content_segment("CH2", background_color="#FF0000")
    strip.add_content_segment("CH3", background_color="#00FF00")
    return strip

@pytest.fixture
def temp_project_file(tmp_path):
    """Create a temporary project file."""
    return tmp_path / "test_project.jlp"
```

### Running Tests

```bash
# Run all tests
make test
uv run pytest

# Run with coverage
make coverage
uv run pytest --cov=jackfield_labeler --cov-report=html

# Run specific test file
uv run pytest tests/test_models/test_label_strip.py

# Run tests matching pattern
uv run pytest -k "test_width"

# Run tests with verbose output
uv run pytest -v

# Run tests and stop on first failure
uv run pytest -x
```

### Test Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--cov=jackfield_labeler",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--strict-markers",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
branch = true
source = ["jackfield_labeler"]
omit = [
    "*/tests/*",
    "*/conftest.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

## Documentation

### Documentation Structure

```
docs/
├── index.md                 # Main documentation index
├── user-guide.md           # User guide
├── architecture.md         # Architecture documentation
├── technical.md            # Technical documentation
├── api-reference.md        # API reference
├── development.md          # This file
└── changelog.md            # Release notes
```

### Writing Documentation

#### Markdown Guidelines

- Use clear, descriptive headings
- Include code examples where appropriate
- Use tables for structured information
- Add diagrams for complex concepts

#### Code Examples

Always test code examples:

```python
# Example: Creating a label strip
from jackfield_labeler.models import LabelStrip

strip = LabelStrip(height=6.0, content_cell_width=12.0)
strip.add_content_segment("CH1")
print(f"Total width: {strip.get_total_width()}mm")  # Output: Total width: 12.0mm
```

#### API Documentation

Use consistent format for API documentation:

```markdown
### method_name

```python
def method_name(self, param1: Type1, param2: Type2 = default) -> ReturnType:
```

Description of what the method does.

**Parameters:**

- `param1` (Type1): Description of parameter
- `param2` (Type2, optional): Description with default value

**Returns:**

- `ReturnType`: Description of return value

**Raises:**

- `ExceptionType`: When this exception is raised

**Example:**

```python
result = obj.method_name("value1", param2="value2")
```

```

### Building Documentation

```bash
# Install documentation dependencies
uv sync

# Serve documentation locally
make docs
uv run mkdocs serve

# Build documentation
uv run mkdocs build

# Deploy to GitHub Pages
uv run mkdocs gh-deploy
```

## Git Workflow

### Branch Strategy

We use a simplified Git Flow:

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/**: Feature development branches
- **hotfix/**: Critical bug fixes
- **release/**: Release preparation branches

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

**Examples:**

```
feat(models): add end segment support

Add EndSegment class and integration with LabelStrip.
Includes validation and serialization support.

Closes #123

fix(pdf): correct rotation calculation

The rotation angle was being calculated incorrectly for
strips wider than the paper. Fixed the algorithm to
properly handle all paper sizes.

docs(api): update LabelStrip documentation

Add missing method documentation and usage examples.
```

### Pull Request Process

1. **Create Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Run Quality Checks**

   ```bash
   make lint
   make typecheck
   make test
   ```

4. **Commit Changes**

   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

5. **Push and Create PR**

   ```bash
   git push origin feature/your-feature-name
   # Create pull request on GitHub
   ```

6. **PR Requirements**
   - All tests pass
   - Code coverage maintained
   - Documentation updated
   - Code review approved

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
```

Install hooks:

```bash
uv run pre-commit install
```

Run manually:

```bash
uv run pre-commit run --all-files
```

## Release Process

### Version Management

We use semantic versioning (SemVer):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps

1. **Prepare Release Branch**

   ```bash
   git checkout -b release/v1.2.0
   ```

2. **Update Version**

   ```toml
   # pyproject.toml
   [project]
   version = "1.2.0"
   ```

3. **Update Changelog**

   ```markdown
   # Changelog
   
   ## [1.2.0] - 2024-01-15
   
   ### Added
   - New feature descriptions
   
   ### Changed
   - Changed feature descriptions
   
   ### Fixed
   - Bug fix descriptions
   ```

4. **Run Full Test Suite**

   ```bash
   make test
   make integration-test
   make lint
   make typecheck
   ```

5. **Create Release PR**
   - Merge release branch to main
   - Tag release: `git tag v1.2.0`
   - Push tags: `git push --tags`

6. **GitHub Release**
   - Create GitHub release from tag
   - Include changelog in release notes
   - Attach any release artifacts

### Automated Releases

GitHub Actions can automate releases:

```yaml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Run tests
        run: |
          uv sync
          uv run pytest
      - name: Build package
        run: uv build
      - name: Create release
        uses: actions/create-release@v1
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
```

## Troubleshooting

### Common Development Issues

#### UV Installation Problems

```bash
# If UV installation fails
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Verify installation
uv --version
```

#### Dependency Conflicts

```bash
# Clear UV cache
uv cache clean

# Reinstall dependencies
rm uv.lock
uv sync
```

#### Test Failures

```bash
# Run tests with verbose output
uv run pytest -v

# Run specific failing test
uv run pytest tests/test_models/test_label_strip.py::test_specific_function -v

# Debug with pdb
uv run pytest --pdb
```

#### Import Errors

```bash
# Verify package installation
uv run python -c "import jackfield_labeler; print('OK')"

# Check Python path
uv run python -c "import sys; print(sys.path)"

# Reinstall in development mode
uv pip install -e .
```

#### PyQt6 Issues

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get install python3-pyqt6

# Install system dependencies (macOS)
brew install pyqt6

# Verify PyQt6 installation
uv run python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"
```

### Performance Issues

#### Slow Tests

```bash
# Run tests in parallel
uv run pytest -n auto

# Profile slow tests
uv run pytest --profile

# Skip slow tests
uv run pytest -m "not slow"
```

#### Memory Usage

```bash
# Monitor memory usage
uv run python -m memory_profiler script.py

# Use memory-efficient alternatives
# - Use generators instead of lists
# - Clear large objects explicitly
# - Use weak references where appropriate
```

### Debugging Tips

#### Logging

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use in code
logger.debug("Debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message")
```

#### PyQt6 Debugging

```python
# Enable Qt logging
import os
os.environ['QT_LOGGING_RULES'] = '*=true'

# Debug signals and slots
from PyQt6.QtCore import QObject
QObject.connect = lambda *args: print(f"Connect: {args}")
```

#### Profiling

```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your code here
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

### Getting Help

#### Documentation

- Read the user guide and API reference
- Check the architecture documentation
- Review existing code for patterns

#### Community

- Check GitHub issues for similar problems
- Search Stack Overflow for PyQt6/Python issues
- Ask questions in GitHub discussions

#### Reporting Issues

When reporting bugs, include:

- Python version and OS
- UV version
- Complete error traceback
- Minimal reproduction case
- Expected vs actual behavior

This development guide should help you get started with contributing to the Jackfield Labeler project. For questions or clarifications, please open an issue on GitHub.
