# AGENTS.md — jackfield-labeler

This file is read by AI agents (Cursor, Claude, etc.) to bootstrap project knowledge.

## Project summary

**jackfield-labeler** is a cross-platform PyQt6 desktop app for designing and printing label strips for 19" rack jackfields, patch panels, and similar audio/broadcast/IT equipment. Users compose strips from segments, configure text/color/formatting, preview live, and export to PDF or PNG (300 DPI).

## Tech stack

| Area | Choice |
|---|---|
| Language | Python 3.12.9 (pinned in `pyproject.toml`) |
| GUI | PyQt6 6.2.0 |
| PDF export | ReportLab ≥ 4.4.1 |
| Dep management | **uv** + hatchling (wheel), PyInstaller (executables) |
| Lint / format | **Ruff** (check + format, enforced via pre-commit) |
| Type checking | mypy (strict on `jackfield_labeler/`) |
| Tests | pytest + pytest-cov |
| Docs | MkDocs + Material + mkdocstrings |

## Dev environment setup

```bash
make install   # uv sync + pre-commit install
make run       # uv run -m jackfield_labeler
```

## Testing

```bash
make test      # pytest + coverage; headless Qt via xvfb
```

On Linux CI, Qt runs headlessly: `QT_QPA_PLATFORM=offscreen xvfb-run -a make test`.
On macOS/Windows development, `make test` works without xvfb.

Test files live in `tests/`. Write plain pytest functions (Arrange-Act-Assert), no class wrappers. The `S101` (assert) rule is suppressed in tests.

## Quality checks

```bash
make check     # what CI runs: uv lock --locked + pre-commit (ruff lint+format)
make mypy      # type-check
make lint      # ruff check only
make fix       # ruff check --fix
```

Pre-commit must pass before every commit. Never use `--no-verify`.

## Architecture

MVC-style layout:

```
jackfield_labeler/
  models/       # Domain models — plain Python, no Qt dependencies
  views/        # PyQt6 widgets; emit pyqtSignal for change events
  controllers/  # Placeholder (thin coordination lives in MainWindow)
  utils/        # pdf_generator, strip_renderer, project_manager, logger
  app.py        # Entry point: QApplication + MainWindow
```

**Key types:**
- `LabelStrip` — top-level model; owns a list of segments and `StripSettings`
- Segment hierarchy: `StartSegment`, `ContentSegment`, `EndSegment`; constructed via `create_segment_from_dict`
- `ProjectManager` — save/load `.jlp` (JSON) project files
- `MainWindow` — coordinates tabs, menus, signals, PDF/PNG export

**Signal flow:** views emit `pyqtSignal` → `MainWindow` routes updates (preview refresh, settings sync). Views do not call each other directly.

**Validation:** centralised in `LabelStrip` (height 5–12 mm, max width 500 mm). Custom exceptions live in `models/exceptions.py`.

## Key directories

| Path | Purpose |
|---|---|
| `jackfield_labeler/` | Main package |
| `tests/` | pytest suite |
| `docs/` | MkDocs source (deployed to GitHub Pages) |
| `examples/` | Sample `.jlp` project files |
| `.github/workflows/` | CI: `main.yml`, `build-executables.yml`, `deploy-docs.yml`, `bump-version.yml` |
| `.github/actions/setup-python-env/` | Reusable composite action (Python + uv + `uv sync --frozen`) |
| `memory-bank/` | Cursor memory-bank files (not part of the runtime app) |

## Dependency management

- Add deps with `uv add <pkg>`; never edit `uv.lock` manually
- `uv sync --frozen` is used in CI to ensure the lock file is respected
- Do **not** use pip, pipenv, or poetry in this project

## Code conventions

- **Line length:** 120 characters (Ruff config)
- **Type hints:** required throughout; mypy strict mode on the main package
- **Imports:** isort-compatible order enforced by Ruff
- **Ruff rule set:** bandit, bugbear, pyupgrade, isort, and others (see `pyproject.toml [tool.ruff.lint]`)
- **No Qt imports in models:** keep `models/` free of PyQt6 to stay testable without a display
- **Logging:** use the project logger (`utils/logger.py`), not bare `print`

## CI overview

| Workflow | Trigger | What it does |
|---|---|---|
| `main.yml` | push / PR to `main` | `make check`, tests (Python 3.12 + 3.13 matrix), docs check |
| `build-executables.yml` | tags `v*.*.*` | PyInstaller on Ubuntu / macOS / Windows → GitHub release |
| `deploy-docs.yml` | push to `main`, manual | MkDocs build → GitHub Pages |
| `bump-version.yml` | manual dispatch | bump2version + tag push |

## Do NOT

- Use `pip install` directly; always go through `uv`
- Commit with `--no-verify`; pre-commit hooks must pass
- Import PyQt6 inside `models/`
- Edit `uv.lock` by hand
- Hardcode `QT_QPA_PLATFORM` in application code (only in CI/test env vars)
