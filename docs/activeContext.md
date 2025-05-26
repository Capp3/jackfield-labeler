# Active Context

## Project Overview

Jackfield Labeler is a desktop application for creating and printing label strips for audio/video jackfields (patch panels). The application allows users to design custom labels with specific dimensions and segment layouts, then outputs them as PDF files ready for printing.

## Current Focus

- Setting up the basic application structure
- Implementing the foundational UI components based on PyQt6

## Project Structure

The project follows an MVC architecture:

- Models: Label strip data structures
- Views: PyQt6 UI components
- Controllers: Logic connecting models and views

## Technical Stack

- Python 3.12+
- PyQt6 for GUI
- PDF generation library (to be determined)
- UV package manager for dependency management

## Development Workflow

- Use UV for all package operations (`uv add`, `uv run`)
- Run application with `uv run -m jackfield_labeler`
- Add dependencies to pyproject.toml with `uv add`
- See docs/development.md for detailed instructions

## Development Status

The project is in the initial setup phase with the environment configured and basic structure being established. The next steps involve implementing the core UI components and models for the label strips.
