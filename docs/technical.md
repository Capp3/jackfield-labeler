# Technical Documentation

## Project Architecture

The jackfield-labeler application is built using Python with PyQt6 for the GUI and will utilize a PDF generation library for output. The application follows a Model-View-Controller (MVC) pattern:

- **Model**: Represents the label strip data structure and business logic
- **View**: The PyQt6-based user interface components
- **Controller**: Handles user interactions and connects model with view

## Dependencies

- **Python**: 3.12+
- **PyQt6**: GUI framework
- **PDF Library**: To be determined (options include ReportLab, FPDF2, or WeasyPrint)

## Package Management

This project uses UV as the package manager instead of pip:

- Dependencies are defined in `pyproject.toml`
- Development dependencies are in the `dev` dependency group
- The lock file (`uv.lock`) ensures reproducible builds
- All package operations should use UV commands (see `docs/development.md`)

## Application Execution

The application should be run using UV:

```bash
uv run -m jackfield_labeler
```

This ensures the correct Python environment and dependencies are used.

## File Structure

```
jackfield_labeler/
├── __init__.py
├── app.py              # Main application entry point
├── models/             # Data models for the label strips
├── views/              # UI components
│   ├── main_window.py  # Main application window
│   ├── designer_tab.py # Label designer tab
│   └── settings_tab.py # Settings configuration tab
├── controllers/        # Application logic connecting models and views
└── utils/              # Helper functions including PDF generation
```

## Technical Decisions

_This section will document key technical decisions as they are made._

## Development Standards

- Code follows PEP 8 guidelines
- Type hints are used throughout the codebase
- Tests are written for all non-UI components
- UV is used for all package management operations
