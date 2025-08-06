# Contributing to `jackfield-labeler`

Contributions are welcome, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

You can contribute in many ways:

# Types of Contributions

## Report Bugs

Report bugs at https://github.com/capp3/jackfield-labeler/issues

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

## Fix Bugs

Look through the GitHub issues for bugs.
Anything tagged with "bug" and "help wanted" is open to whoever wants to implement a fix for it.

## Implement Features

Look through the GitHub issues for features.
Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

## Write Documentation

jackfield-labeler could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

## Submit Feedback

The best way to send feedback is to file an issue at https://github.com/capp3/jackfield-labeler/issues.

If you are proposing a new feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

# Get Started!

Ready to contribute? Here's how to set up `jackfield-labeler` for local development.
Please note this documentation assumes you already have `uv` and `Git` installed and ready to go.

1. Fork the `jackfield-labeler` repo on GitHub.

2. Clone your fork locally:

```bash
cd <directory_in_which_repo_should_be_created>
git clone git@github.com:YOUR_NAME/jackfield-labeler.git
```

3. Set up the development environment:

```bash
cd jackfield-labeler
make dev
```

This single command will:
- Install all dependencies using `uv sync`
- Install pre-commit hooks
- Set up your development environment

4. Create a branch for local development:

```bash
git checkout -b name-of-your-bugfix-or-feature
```

Now you can make your changes locally.

5. Don't forget to add test cases for your added functionality to the `tests` directory.

6. When you're done making changes, run the quality checks:

```bash
make ci
```

This will run:
- Code quality checks (linting, formatting, type checking)
- Tests with coverage
- Documentation build verification

7. For a full development cycle (clean, install, test, build):

```bash
make all
```

8. To run the application locally:

```bash
make run
```

9. To build documentation and serve it locally:

```bash
make docs-serve
```

# Development Commands

The project uses a Lean Makefile for all development tasks. Run `make help` to see all available commands:

- `make dev` - Set up development environment
- `make check` - Run quality checks
- `make test` - Run tests with coverage
- `make test-watch` - Run tests in watch mode
- `make run` - Run the application
- `make build` - Build wheel distribution
- `make build-exe` - Build executable (requires PyInstaller)
- `make clean` - Clean build artifacts
- `make docs-build` - Build documentation
- `make docs-serve` - Serve documentation locally
- `make docs-check` - Check documentation build
- `make ci` - Run all CI checks locally
- `make all` - Run full development cycle
- `make release VERSION=1.0.0` - Create a new release

# Pull Request Process

1. Update the README.md with details of changes to the interface, if applicable.
2. Update the documentation in the `docs/` directory if needed.
3. The PR will be merged once you have the sign-off of at least one other developer.
4. The PR will be automatically tested by GitHub Actions.

# Code Style

- Use `ruff` for linting and formatting (configured in `pyproject.toml`)
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions small and focused
- Write tests for new functionality

# Testing

- Tests are located in the `tests/` directory
- Run tests with `make test`
- Run tests in watch mode with `make test-watch`
- Ensure all tests pass before submitting a PR
- Add tests for new functionality

# Documentation

- Documentation is built with MkDocs
- Source files are in the `docs/` directory
- Build documentation with `make docs-build`
- Serve documentation locally with `make docs-serve`
- Check documentation build with `make docs-check`

# Release Process

1. Update version in `pyproject.toml`
2. Create a release with `make release VERSION=x.y.z`
3. GitHub Actions will automatically build and release executables
4. Documentation will be automatically deployed to GitHub Pages
