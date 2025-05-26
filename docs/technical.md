# Technical Documentation

## Project Overview

The Jackfield Labeler is a professional desktop application for creating custom label strips for 19" equipment rack jackfields, patch panels, and audio equipment. Built with Python and PyQt6, it provides an intuitive interface for designing labels with precise dimensions and professional output quality.

## Architecture

### Design Pattern: Model-View-Controller (MVC)

The application follows a clean MVC architecture with PyQt6's signal-slot mechanism providing loose coupling between components:

- **Models** (`jackfield_labeler/models/`): Pure data structures and business logic
- **Views** (`jackfield_labeler/views/`): PyQt6-based user interface components
- **Utils** (`jackfield_labeler/utils/`): Specialized utilities for PDF generation, rendering, and file management
- **Controllers** (`jackfield_labeler/controllers/`): Minimal coordination layer (Qt handles most controller logic)

### Signal-Driven Communication

```python
# Example signal flow
LabelStrip.strip_changed.emit()  # Model emits change
    ↓
MainWindow._on_strip_changed()   # Main window receives signal
    ↓
PreviewTab.update_preview()      # Preview updates automatically
```

## Core Dependencies

### Runtime Dependencies

- **Python**: 3.12+ (required for modern type hints and performance)
- **PyQt6**: 6.9.0+ (cross-platform GUI framework)
- **ReportLab**: 4.4.1+ (professional PDF generation)

### Development Dependencies

- **UV**: Modern Python package manager (replaces pip)
- **pytest**: Testing framework with coverage reporting
- **mypy**: Static type checking for code quality
- **ruff**: Fast Python linter and formatter
- **pre-commit**: Git hooks for code quality enforcement

## Package Management

### UV Package Manager

This project uses UV instead of pip for several advantages:

```bash
# Add runtime dependency
uv add package-name

# Add development dependency  
uv add --group dev package-name

# Install all dependencies
uv sync

# Run application
uv run -m jackfield_labeler

# Run tests
uv run pytest
```

### Dependency Configuration

Dependencies are defined in `pyproject.toml`:

```toml
[project]
dependencies = [
    "pyqt6>=6.9.0",
    "reportlab>=4.4.1",
]

[dependency-groups]
dev = [
    "pytest>=8.3.5",
    "mypy>=1.15",
    "ruff>=0.11.11",
    # ... other dev dependencies
]
```

## Application Structure

### Directory Layout

```
jackfield_labeler/
├── __init__.py              # Package initialization
├── __main__.py              # Entry point for -m execution
├── app.py                   # Application setup and configuration
├── models/                  # Data models and business logic
│   ├── __init__.py          # Model exports
│   ├── label_strip.py       # Core label strip model
│   ├── segment_types.py     # Segment implementations
│   ├── segment.py           # Base segment class
│   ├── strip_settings.py    # Configuration model
│   ├── color.py            # Color definitions and utilities
│   └── text_format.py      # Text formatting enumerations
├── views/                   # User interface components
│   ├── __init__.py          # View exports
│   ├── main_window.py       # Main application window
│   ├── designer_tab.py      # Label design interface
│   ├── preview_tab.py       # Preview and export interface
│   └── settings_tab.py      # Settings configuration
├── utils/                   # Utility modules
│   ├── __init__.py          # Utility exports
│   ├── pdf_generator.py     # PDF generation engine
│   ├── strip_renderer.py    # PNG rendering engine
│   └── project_manager.py   # Project save/load functionality
└── controllers/             # Application logic coordination
    └── __init__.py          # Controller exports (minimal)
```

### Code Statistics

- **Total Application Code**: ~3,300 lines
- **Test Code**: ~350 lines
- **Documentation**: ~2,000 lines
- **Configuration**: ~120 lines

## Data Models

### LabelStrip (`models/label_strip.py`)

The central data model representing a complete label strip design.

```python
@dataclass
class LabelStrip(QObject):
    height: float = 6.0
    content_cell_width: float = 12.0
    segments: List[Segment] = field(default_factory=list)
    settings: StripSettings = field(default_factory=StripSettings)
    
    # Signals for UI updates
    strip_changed = pyqtSignal()
    segment_added = pyqtSignal(int)
    segment_removed = pyqtSignal(int)
```

**Key Features:**
- Immutable design with builder pattern
- Signal emission for UI updates
- Automatic width calculation
- Serialization support for project files

### Segment Types (`models/segment_types.py`)

Three types of segments with polymorphic behavior:

```python
class StartSegment(Segment):
    """Optional start label (e.g., 'INPUT')"""
    
class ContentSegment(Segment):
    """Main content cells (e.g., 'CH1', 'CH2')"""
    
class EndSegment(Segment):
    """Optional end label (e.g., 'OUTPUT')"""
```

**Design Patterns:**
- Factory pattern for creation from dictionaries
- Strategy pattern for type-specific behavior
- Builder pattern for complex construction

### StripSettings (`models/strip_settings.py`)

Configuration model with comprehensive settings:

```python
@dataclass
class StripSettings:
    paper_size: PaperSize = PaperSize.A3
    page_margins: PageMargins = field(default_factory=PageMargins)
    rotation_angle: float = 60.0
    default_font_name: str = "Arial"
    default_font_size: float = 8.0
    default_text_color: str = "#000000"
    default_background_color: str = "#FFFFFF"
```

## User Interface Architecture

### Main Window (`views/main_window.py`)

Central coordination point for the application:

```python
class MainWindow(QMainWindow):
    def __init__(self):
        # Tab management
        self.designer_tab = DesignerTab()
        self.preview_tab = PreviewTab()
        self.settings_tab = SettingsTab()
        
        # Signal routing
        self.designer_tab.strip_changed.connect(self.preview_tab.update_preview)
        self.settings_tab.settings_changed.connect(self.designer_tab.apply_settings)
```

**Responsibilities:**
- Tab coordination and signal routing
- Menu bar and global actions
- Project state management
- File operations and dialogs

### Designer Tab (`views/designer_tab.py`)

Main workspace with sophisticated table management:

```python
class DesignerTab(QWidget):
    def __init__(self):
        self.control_panel = self._create_control_panel()
        self.segment_table = self._create_segment_table()
        self.action_buttons = self._create_action_buttons()
        
    def _create_segment_table(self):
        """Creates table with custom delegates for colors and formatting"""
        table = QTableWidget()
        table.setItemDelegate(ColorButtonDelegate())
        return table
```

**Key Features:**
- Custom table delegates for color pickers
- Real-time validation and feedback
- Dynamic row management
- Signal emission for all changes

### Preview Tab (`views/preview_tab.py`)

Real-time preview with high-quality rendering:

```python
class PreviewTab(QWidget):
    def __init__(self):
        self.preview_widget = StripPreviewWidget()
        self.info_panel = StripInfoPanel()
        self.export_controls = self._create_export_controls()
        
    def update_preview(self, label_strip: LabelStrip):
        """Updates preview with auto-scaling"""
        pixmap = self.renderer.render_to_pixmap(label_strip, self.scale_factor)
        self.preview_widget.setPixmap(pixmap)
```

### Settings Tab (`views/settings_tab.py`)

Comprehensive settings interface with grouped controls:

```python
class SettingsTab(QWidget):
    def __init__(self):
        self.paper_group = PaperGroup()
        self.rotation_group = RotationGroup()
        self.font_group = FontGroup()
        self.color_group = ColorGroup()
```

## Utility Modules

### PDF Generator (`utils/pdf_generator.py`)

Professional PDF generation with ReportLab:

```python
class PDFGenerator:
    def generate_pdf(self, label_strip: LabelStrip, filename: str, 
                    rotation_angle: float | None = None) -> bool:
        """Generates high-quality PDF with precise positioning"""
        c = canvas.Canvas(filename, pagesize=self.paper_size)
        
        # Apply rotation and positioning
        c.saveState()
        c.translate(center_x, center_y)
        c.rotate(rotation_angle)
        
        # Render segments with exact dimensions
        for segment in label_strip.segments:
            self._draw_segment(c, segment, x_offset)
            
        c.restoreState()
        c.save()
```

**Technical Features:**
- No automatic scaling (preserves exact dimensions)
- Center-to-center positioning algorithm
- Support for all standard paper sizes
- Color space conversion (RGB to ReportLab format)
- Font handling with fallbacks

### Strip Renderer (`utils/strip_renderer.py`)

High-quality PNG rendering with Qt:

```python
class StripRenderer:
    def render_to_pixmap(self, label_strip: LabelStrip, 
                        scale_factor: float = 1.0) -> QPixmap:
        """Renders strip to QPixmap for preview or export"""
        width_px = int(total_width_mm * self.pixels_per_mm * scale_factor)
        height_px = int(label_strip.height * self.pixels_per_mm * scale_factor)
        
        pixmap = QPixmap(width_px, height_px)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Render each segment
        for segment in label_strip.segments:
            self._draw_segment(painter, segment, x_offset, scale_factor)
```

**Features:**
- Configurable DPI (default 300 for print quality)
- Anti-aliased rendering
- Scalable output for different use cases
- Qt-based rendering pipeline

### Project Manager (`utils/project_manager.py`)

Robust project file management:

```python
class ProjectManager:
    @staticmethod
    def save_project(label_strip: LabelStrip, filename: str) -> bool:
        """Saves project in JSON format with validation"""
        project_data = {
            "version": "1.0",
            "application": "Jackfield Labeler",
            "label_strip": label_strip.to_dict(),
            "metadata": {
                "created_by": "Jackfield Labeler",
                "file_format_version": "1.0"
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(project_data, f, indent=2)
```

**File Format Features:**
- JSON-based for human readability
- Version control for future compatibility
- Comprehensive validation
- Error handling and recovery

## Technical Decisions

### 1. PyQt6 vs Other GUI Frameworks

**Chosen**: PyQt6
**Rationale**: 
- Mature, stable framework with excellent documentation
- Native look and feel on all platforms
- Powerful signal-slot mechanism for loose coupling
- Rich widget set including advanced table features
- Professional licensing available

### 2. ReportLab vs Other PDF Libraries

**Chosen**: ReportLab
**Rationale**:
- Industry standard for professional PDF generation
- Precise control over positioning and graphics
- Excellent font handling and color management
- Vector-based output for scalability
- Extensive documentation and community support

### 3. UV vs pip for Package Management

**Chosen**: UV
**Rationale**:
- Significantly faster than pip
- Better dependency resolution
- Built-in virtual environment management
- Modern approach to Python packaging
- Excellent compatibility with existing tools

### 4. JSON vs Binary for Project Files

**Chosen**: JSON
**Rationale**:
- Human-readable for debugging and inspection
- Version control friendly
- Easy to parse and validate
- Cross-platform compatibility
- Future-proof format

### 5. Signal-Slot vs Direct Method Calls

**Chosen**: Signal-Slot
**Rationale**:
- Loose coupling between components
- Automatic UI updates
- Thread-safe communication
- Extensible for future features
- Qt's recommended pattern

## Performance Considerations

### 1. Preview Rendering Optimization

```python
class PreviewTab:
    def __init__(self):
        self._preview_cache = {}
        self._update_timer = QTimer()
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._do_update_preview)
    
    def update_preview(self):
        """Debounced preview updates to avoid excessive rendering"""
        self._update_timer.start(100)  # 100ms delay
```

### 2. Memory Management

- Pixmap caching for preview rendering
- Automatic cleanup of temporary objects
- Efficient signal/slot connections
- Lazy loading of UI components

### 3. Startup Performance

- Minimal imports in `__init__.py`
- Deferred widget creation
- Fast application startup (~1-2 seconds)

## Testing Strategy

### Unit Tests (`tests/`)

```python
def test_label_strip_width_calculation():
    """Test that total width is calculated correctly"""
    strip = LabelStrip(content_cell_width=10.0)
    strip.add_content_segment("CH1")
    strip.add_content_segment("CH2")
    
    assert strip.get_total_width() == 20.0
```

**Coverage Areas:**
- Model logic and calculations
- Utility functions
- File format validation
- Color conversion algorithms

### Integration Tests

```python
def test_pdf_generation_integration():
    """Test complete PDF generation workflow"""
    strip = create_test_strip()
    generator = PDFGenerator()
    
    success = generator.generate_pdf(strip, "test.pdf")
    assert success
    assert os.path.exists("test.pdf")
```

### Test Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=jackfield_labeler --cov-report=html"

[tool.coverage.run]
branch = true
source = ["jackfield_labeler"]
```

## Code Quality Standards

### Type Checking with mypy

```toml
[tool.mypy]
files = ["jackfield_labeler"]
disallow_untyped_defs = true
disallow_any_unimported = true
no_implicit_optional = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true
```

### Linting with ruff

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

### Pre-commit Hooks

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

## Security Considerations

### 1. File Handling Security

```python
def validate_project_file(filename: str) -> bool:
    """Validates project file before loading"""
    if not filename.endswith('.jlp'):
        return False
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return validate_project_structure(data)
    except (json.JSONDecodeError, IOError):
        return False
```

### 2. Input Validation

- All user inputs are validated at the UI level
- Model-level validation for business logic
- Range checking for numeric inputs
- Text sanitization for file operations

### 3. PDF Generation Security

- Safe text rendering (no code execution)
- Resource limits for large documents
- Error containment and recovery
- Temporary file cleanup

## Deployment Considerations

### 1. Cross-Platform Compatibility

**Supported Platforms:**
- Windows 10/11 (x64)
- macOS 10.15+ (Intel and Apple Silicon)
- Linux (Ubuntu 20.04+, other distributions)

### 2. Distribution Methods

**Current**: Source distribution with UV
**Future**: 
- PyInstaller executables
- Platform-specific packages (MSI, DMG, DEB)
- Snap/Flatpak packages

### 3. System Requirements

**Minimum:**
- Python 3.12+
- 512MB RAM
- 100MB disk space
- Display: 1024x768

**Recommended:**
- Python 3.12+
- 2GB RAM
- 500MB disk space
- Display: 1920x1080

## Future Technical Enhancements

### 1. Plugin Architecture

```python
class PluginInterface:
    def get_segment_types(self) -> List[Type[Segment]]:
        """Return custom segment types"""
        
    def get_export_formats(self) -> List[ExportFormat]:
        """Return custom export formats"""
```

### 2. Advanced Rendering

- 3D preview capabilities
- Print simulation with color management
- Advanced typography features
- Custom font embedding

### 3. Performance Optimizations

- Multi-threaded rendering
- GPU acceleration for preview
- Incremental updates
- Background processing

### 4. Cloud Integration

- Project synchronization
- Collaborative editing
- Template sharing
- Online backup

## Debugging and Diagnostics

### 1. Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/jackfield_labeler.log'),
        logging.StreamHandler()
    ]
)
```

### 2. Debug Mode

```bash
# Enable debug mode
export JACKFIELD_DEBUG=1
uv run -m jackfield_labeler
```

### 3. Performance Profiling

```python
# Profile critical sections
import cProfile
import pstats

def profile_pdf_generation():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # PDF generation code
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

## Maintenance and Updates

### 1. Dependency Updates

```bash
# Check for outdated dependencies
uv pip list --outdated

# Update dependencies
uv sync --upgrade
```

### 2. Code Quality Monitoring

```bash
# Run all quality checks
make lint
make typecheck
make test
make coverage
```

### 3. Documentation Updates

- Keep documentation in sync with code changes
- Update API documentation automatically
- Maintain changelog for releases
- Review and update user guide regularly
