# Active Context

## Project Overview

Jackfield Labeler is a **feature-complete desktop application** for creating and printing custom label strips for audio/video jackfields (patch panels). The application provides a professional interface for designing labels with specific dimensions and segment layouts, then outputs them as high-quality PDF files ready for printing.

## Current Development Status

The project has reached **beta completion** with all core functionality implemented and working. The application is ready for final polish and version 1.0 release.

### What's Working

- ✅ Complete GUI with Designer, Settings, and Preview tabs
- ✅ Full label strip design capabilities with segment customization
- ✅ Professional PDF generation with intelligent rotation
- ✅ Project save/load functionality with `.jlp` format
- ✅ Real-time preview and PNG export
- ✅ Comprehensive test suite with good coverage

### Current Focus Areas

- 🟡 Final UI polish and visual improvements
- 🟡 Multi-page support for extra-large strips
- 🟡 Enhanced preview with rotation visualization
- ⏳ Version 1.0 release preparation
- ⏳ Executable distribution for all platforms

## Technical Architecture

The project follows a clean **Model-View-Controller (MVC) architecture**:

- **Models** (`jackfield_labeler/models/`): Data structures for label strips, segments, and settings
- **Views** (`jackfield_labeler/views/`): PyQt6-based user interface components
- **Utils** (`jackfield_labeler/utils/`): PDF generation, rendering, and project management
- **Controllers**: Logic is integrated within views using PyQt6's signal-slot mechanism

## Technology Stack

- **Python 3.12+** with comprehensive type hints
- **PyQt6** (≥6.9.0) for cross-platform GUI
- **ReportLab** (≥4.4.1) for professional PDF generation
- **UV** package manager for fast dependency management
- **Ruff** for code quality and formatting
- **pytest** for testing framework

## Development Workflow

- **Package Management**: Use UV for all operations (`uv add`, `uv run`, `uv sync`)
- **Application Execution**: `uv run -m jackfield_labeler`
- **Testing**: `uv run pytest` for test suite execution
- **Code Quality**: `uv run ruff check` and `uv run ruff format`
- **Documentation**: See `docs/development.md` for detailed instructions

## Codebase Statistics

- **Main Application**: ~3,500 lines of Python code across 21 files
- **Test Suite**: ~315 lines of tests
- **Dependencies**: 3 core runtime dependencies, 9 development dependencies
- **Architecture**: Clean MVC separation with well-defined interfaces

## Key Features Implemented

### Core Functionality

- Label strip design with customizable segments
- Real-time preview and validation
- Professional PDF generation with rotation
- Project save/load with JSON serialization
- Cross-platform compatibility (Windows, macOS, Linux)

### User Interface

- Intuitive tabbed interface (Designer, Settings, Preview)
- Dynamic segment table with inline editing
- Color pickers and formatting options
- Responsive design with immediate feedback
- Professional styling and layout

### Output Capabilities

- High-quality PDF generation using ReportLab
- Intelligent rotation for optimal paper usage
- Multiple paper size support (A0-A4, Letter, Legal, Tabloid)
- PNG export with 300 DPI resolution
- Center-to-center positioning algorithm

## Development Priorities

1. **Immediate**: Complete version 1.0 release preparation
2. **Short-term**: Create standalone executables for distribution
3. **Medium-term**: Enhance documentation and user guides
4. **Long-term**: Community release and ongoing maintenance

## Quality Assurance

- **Code Quality**: PEP 8 compliance enforced by Ruff
- **Type Safety**: Comprehensive type hints throughout
- **Testing**: Good test coverage for core functionality
- **Documentation**: Google-style docstrings and comprehensive guides
- **Error Handling**: Robust exception handling with custom error types
