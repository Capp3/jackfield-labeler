# jackfield-labeler

[![Release](https://img.shields.io/github/v/release/capp3/jackfield-labeler)](https://img.shields.io/github/v/release/capp3/jackfield-labeler)
[![Build status](https://img.shields.io/github/actions/workflow/status/capp3/jackfield-labeler/main.yml?branch=main)](https://github.com/capp3/jackfield-labeler/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/capp3/jackfield-labeler/branch/main/graph/badge.svg)](https://codecov.io/gh/capp3/jackfield-labeler)
[![Commit activity](https://img.shields.io/github/commit-activity/m/capp3/jackfield-labeler)](https://img.shields.io/github/commit-activity/m/capp3/jackfield-labeler)
[![License](https://img.shields.io/github/license/capp3/jackfield-labeler)](https://img.shields.io/github/license/capp3/jackfield-labeler)

A utility to create strip labels for jackfields

- **Github repository**: <https://github.com/capp3/jackfield-labeler/>
- **Documentation** <https://capp3.github.io/jackfield-labeler/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:capp3/jackfield-labeler.git
git push -u origin main
```

### 2. Set Up Your Development Environment

This project uses UV instead of pip for package management. Install the environment and the pre-commit hooks with:

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Running the Application

To run the application:

```bash
make run
# or directly with UV
uv run -m jackfield_labeler
```

### 5. Development

For complete development instructions, see [docs/development.md](docs/development.md).

### 6. Commit the changes

Lastly, commit the changes made by the setup steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/codecov/).

## Dependencies

### Core Dependencies

- **Python**: 3.12 or higher
- **PyQt6**: 6.9.0 or higher - Qt GUI framework for Python

### Development Dependencies

- **UV**: Package manager (alternative to pip)
- **pytest**: For unit testing
- **pre-commit**: Git hook scripts for code quality checks
- **tox-uv**: UV integration for tox
- **mypy**: Static type checker
- **pytest-cov**: Test coverage reporting
- **ruff**: Fast Python linter and formatter
- **mkdocs**: Documentation generator
- **mkdocs-material**: Material theme for MkDocs
- **mkdocstrings**: Auto-generate API documentation

### System Dependencies

When running in a container or on Linux systems, these additional packages may be required:

- **libgl1-mesa-glx**: OpenGL library required for PyQt
- **libxkbcommon0**: X keyboard common library

## Releasing a new version

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
