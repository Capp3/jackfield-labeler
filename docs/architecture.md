# Architecture Documentation

## Overview

The Jackfield Labeler application is built using a clean Model-View-Controller (MVC) architecture with PyQt6 for the user interface and ReportLab for PDF generation. The application is designed to be maintainable, extensible, and user-friendly, with approximately 3,300 lines of application code and comprehensive test coverage.

## Architecture Principles

### 1. Separation of Concerns

- **Models**: Pure data structures and business logic, independent of UI
- **Views**: PyQt6 widgets responsible only for presentation and user interaction
- **Utils**: Specialized utilities for PDF generation, rendering, and file management
- **Controllers**: Coordination between models and views (minimal in this Qt-based architecture)

### 2. Data Flow

```bash
User Input → View → Model Update → Signal Emission → View Update → Preview/Export
```

### 3. Signal-Driven Architecture

The application uses PyQt6's signal-slot mechanism for loose coupling between components:

- Models emit signals when data changes
- Views listen to model signals and update accordingly
- Cross-tab communication through main window signal routing

## Core Components

### Models (`jackfield_labeler/models/`)

#### LabelStrip (`label_strip.py`)

The central data model representing a complete label strip design.

**Key Features:**

- Manages collections of segments (start, content, end)
- Calculates total width and validates dimensions
- Provides serialization/deserialization for project files
- Maintains strip settings and configuration

**Key Methods:**

- `get_total_width()`: Calculates total strip width
- `set_content_segment_count()`: Manages content segment collection
- `set_start_segment()` / `set_end_segment()`: Configure optional segments
- `to_dict()` / `from_dict()`: Serialization support
- `validate()`: Comprehensive validation with error reporting

**Validation Rules:**

- Height constraints: 5.0mm - 12.0mm
- Maximum total width: 500.0mm
- Positive segment widths
- Content cell width precision to 3 decimal places

#### Segments (`segment_types.py`, `segment.py`)

Individual label segments with different types and properties.

**Segment Types:**

- **StartSegment**: Optional start label (e.g., "INPUT")
- **ContentSegment**: Main content cells (e.g., "CH1", "CH2")
- **EndSegment**: Optional end label (e.g., "OUTPUT")

**Properties:**

- Width (mm), Text, Text Color, Background Color, Text Format
- Type-specific validation and behavior
- Immutable design with builder pattern

**Factory Pattern:**

```python
def create_segment_from_dict(data: Dict[str, Any]) -> Segment:
    """Creates appropriate segment type from dictionary data"""
```

#### StripSettings (`strip_settings.py`)

Configuration model for paper size, margins, rotation, and defaults.

**Settings Categories:**

- **Paper Settings**: Size (A0-A4, Letter, Legal, Tabloid), margins
- **Rotation Settings**: Angle (0°-360°), with 60° default
- **Font Settings**: Default font family and size
- **Color Settings**: Default text and background colors

**Default Values:**

- Paper Size: A3 (297 × 420 mm)
- Rotation: 60° (optimized for long strips)
- Margins: 10mm on all sides
- Font: Arial, 8pt
- Colors: Black text on white background

#### Supporting Models

- **Color** (`color.py`): RGB color model with standard color constants
- **TextFormat** (`text_format.py`): Enumeration for text formatting options
- **PageMargins**: Dataclass for page margin configuration
- **PaperSize**: Enumeration for standard paper sizes

### Views (`jackfield_labeler/views/`)

#### MainWindow (`main_window.py`)

The primary application window that coordinates all tabs and provides global functionality.

**Responsibilities:**

- Tab management (Designer, Preview, Settings)
- Menu bar and file operations (New, Open, Save, Export)
- Project state tracking (unsaved changes, window title)
- Signal routing between tabs
- Global error handling and user feedback

**Key Features:**

- Project lifecycle management
- Cross-tab communication via signal routing
- Status bar updates and user feedback
- File dialog management with proper filtering
- Window title updates showing project state

**Signal Routing:**

```python
# Example signal connections
self.designer_tab.strip_changed.connect(self.preview_tab.update_preview)
self.settings_tab.settings_changed.connect(self.designer_tab.apply_settings)
```

#### DesignerTab (`designer_tab.py`)

The main workspace for creating and editing label strips.

**Components:**

- **ControlPanel**: Strip dimensions and global settings
- **SegmentTable**: Spreadsheet-like interface for segment editing
- **ActionButtons**: Add/remove segments, generate PDF, save/load

**Key Features:**

- Real-time validation and feedback
- Dynamic table management with custom delegates
- Color picker integration
- Signal emission for all changes
- Automatic UI updates when model changes

**Table Management:**

- Custom delegates for color buttons and format selection
- Dynamic row addition/removal
- Cell-level validation and feedback
- Tab navigation and keyboard shortcuts

#### PreviewTab (`preview_tab.py`)

Real-time visual preview and PNG export functionality.

**Components:**

- **StripPreviewWidget**: Scalable visual representation
- **StripInfoPanel**: Dimensions and metadata display
- **Export Controls**: PNG export with quality settings

**Key Features:**

- Auto-scaling preview with scroll support
- High-resolution rendering (300 DPI)
- Direct PNG export capability
- Responsive design that adapts to window size
- Real-time updates when strip changes

**Rendering Pipeline:**

```python
# Preview update flow
strip_changed → calculate_scale_factor → render_to_pixmap → update_display
```

#### SettingsTab (`settings_tab.py`)

Global configuration interface for paper, rotation, and default settings.

**Setting Groups:**

- **PaperGroup**: Paper size and margin controls
- **RotationGroup**: Rotation angle with preset buttons
- **FontGroup**: Font family and size selection
- **ColorGroup**: Default color selection

**Key Features:**

- Immediate setting application
- Preset rotation buttons (0°, 90°, 180°, 270°)
- Font dialog integration
- Color picker widgets
- Settings persistence with project files

### Utils (`jackfield_labeler/utils/`)

#### PDFGenerator (`pdf_generator.py`)

High-quality PDF generation with rotation and positioning.

**Key Features:**

- Support for all standard paper sizes
- Configurable rotation (0°-360°)
- Center-to-center positioning algorithm
- No automatic scaling (preserves exact dimensions)
- Color conversion and font handling
- Professional output quality

**Technical Implementation:**

- Uses ReportLab Canvas for precise control
- Graphics state management for rotation
- Millimeter-to-point conversion (1mm = 2.834645669 points)
- Text centering and formatting
- Error handling and validation

**Positioning Algorithm:**

```python
# Center-to-center positioning
center_x = (paper_width - total_width) / 2
center_y = (paper_height - strip_height) / 2

# Apply rotation around center point
canvas.translate(center_x, center_y)
canvas.rotate(rotation_angle)
```

#### StripRenderer (`strip_renderer.py`)

PNG rendering and preview generation engine.

**Key Features:**

- Configurable DPI (default 300)
- Scalable preview rendering
- Anti-aliased output
- Qt-based rendering pipeline

**Use Cases:**

- Preview tab visualization
- PNG export functionality
- Print preview generation
- High-resolution output for documentation

**Rendering Process:**

```python
# High-level rendering flow
calculate_dimensions → create_pixmap → setup_painter → render_segments → return_pixmap
```

#### ProjectManager (`project_manager.py`)

Project file management with `.jlp` format support.

**Key Features:**

- JSON-based file format
- Version control and validation
- Comprehensive error handling
- Metadata management

**File Format Structure:**

```json
{
  "version": "1.0",
  "application": "Jackfield Labeler",
  "label_strip": {
    "height": 6.0,
    "content_cell_width": 12.0,
    "segments": [...],
    "settings": {...}
  },
  "metadata": {
    "created_by": "Jackfield Labeler",
    "file_format_version": "1.0"
  }
}
```

**Validation Features:**

- JSON schema validation
- Version compatibility checking
- Data integrity verification
- Graceful error handling and recovery

#### Logger (`logger.py`)

Centralized logging configuration and management for the entire application.

**Key Features:**

- Module-level logger factory
- Configurable log levels (DEBUG, INFO, WARNING, ERROR)
- Dual output: console (always) + optional file
- Rotating file handler (10MB, 3 backups)
- Cross-platform log file management
- Integration with QSettings for persistence

**API:**

```python
from jackfield_labeler.utils.logger import get_logger, configure_logging

# Get module-level logger
logger = get_logger(__name__)

# Configure logging system
configure_logging(
    level="INFO",                # Log level
    log_to_file=True,            # Enable file output
    log_file_path="/path/to/log" # File path
)

# Use logger
logger.info("Application started")
logger.warning("Validation failed")
logger.error("Error occurred", exc_info=True)
```

**Log Format:**

```
YYYY-MM-DD HH:MM:SS - module.name - LEVEL - Message
```

**Integration Points:**

- Application startup (`app.py`): Initializes logging from QSettings
- Settings tab: UI controls for log configuration
- All error handlers: Consistent error logging with context
- File operations: Operation tracking and error reporting

## Data Flow Architecture

### 1. User Interaction Flow

```bash
User Input (Designer Tab)
    ↓
Control Panel / Segment Table
    ↓
Model Update (LabelStrip)
    ↓
Signal Emission (strip_changed)
    ↓
Preview Update (Preview Tab)
    ↓
Visual Feedback
```

### 2. Settings Flow

```bash
Settings Tab Input
    ↓
StripSettings Model Update
    ↓
Signal Emission (settings_changed)
    ↓
Designer Tab Update
    ↓
Model Application
    ↓
Preview Refresh
```

### 3. Export Flow

```bash
Export Request (Menu/Button)
    ↓
Current Model State
    ↓
Generator (PDF/PNG)
    ↓
File Output
    ↓
User Feedback
```

### 4. Project Management Flow

```bash
Save: Model → Serialization → JSON → File
Load: File → JSON → Validation → Model → UI Update
```

## Design Patterns

### 1. Model-View-Controller (MVC)

- Clear separation between data, presentation, and logic
- Models are UI-independent and testable
- Views handle only presentation concerns
- Controllers coordinate interactions (minimal due to Qt's architecture)

### 2. Observer Pattern

- PyQt6 signals and slots for loose coupling
- Models notify views of changes automatically
- Views update reactively to model changes
- Extensible for future features

### 3. Strategy Pattern

- Different segment types with common interface
- Pluggable PDF generation strategies
- Configurable rendering approaches
- Extensible for new segment types

### 4. Builder Pattern

- Segment creation with fluent interface
- Complex object construction with validation
- Step-by-step object building
- Validation during construction process

### 5. Factory Pattern

- Segment creation from dictionaries
- Type-specific instantiation based on data
- Extensible for new segment types
- Centralized object creation logic

### 6. Command Pattern

- File operations (save, load, export)
- Undo/redo capability (future enhancement)
- Operation encapsulation
- Error handling and rollback

## Error Handling Strategy

### 1. Validation Layers

- **Input Validation**: UI-level validation with immediate feedback
- **Model Validation**: Business logic validation in models
- **Output Validation**: Generation-time validation

### 2. Error Recovery

- Graceful degradation for invalid inputs
- Default value fallbacks
- User-friendly error messages
- Automatic correction where possible

### 3. Exception Handling

- Try-catch blocks around critical operations
- Logging for debugging and diagnostics
- User notification for errors
- Resource cleanup in finally blocks

### 4. Validation Examples

```python
# Model validation
def validate(self) -> list[str]:
    """Returns list of validation errors"""
    errors = []
    if self.height < self.MIN_HEIGHT:
        errors.append(f"Height {self.height}mm is below minimum {self.MIN_HEIGHT}mm")
    return errors

# UI validation
def _validate_input(self, value: str) -> bool:
    """Validates user input with immediate feedback"""
    try:
        float_value = float(value)
        return float_value > 0
    except ValueError:
        return False
```

## Performance Considerations

### 1. Lazy Loading

- Preview updates only when visible
- Deferred PDF generation until requested
- On-demand rendering for large strips

### 2. Caching

- Rendered preview caching for unchanged strips
- Font metrics caching for text rendering
- Color conversion caching for repeated colors

### 3. Signal Optimization

- Batched updates for multiple changes
- Debounced preview updates to avoid excessive rendering
- Efficient signal routing to minimize overhead

### 4. Memory Management

- Automatic cleanup of temporary objects
- Efficient pixmap handling
- Resource management for file operations

## Extensibility Points

### 1. New Segment Types

- Implement Segment base class
- Add to factory method in `create_segment_from_dict`
- Update UI components for new properties
- Add validation rules

### 2. Export Formats

- Implement generator interface
- Add to export menu and file dialogs
- Integrate with existing error handling
- Add format-specific settings

### 3. Paper Sizes

- Add to PaperSize enumeration
- Update size mapping in PDFGenerator
- Test with rotation logic
- Validate with margin calculations

### 4. Color Palettes

- Extend StandardColor enumeration
- Add to color picker widgets
- Update serialization format
- Maintain backward compatibility

## Testing Strategy

### 1. Unit Tests

- Model logic testing with comprehensive coverage
- Utility function testing with edge cases
- Validation testing with invalid inputs
- Serialization testing with various formats

### 2. Integration Tests

- Component interaction testing
- Signal/slot communication testing
- File format compatibility testing
- End-to-end workflow testing

### 3. UI Tests

- Widget behavior testing
- User interaction simulation
- Visual regression testing (future)
- Accessibility testing (future)

### 4. Test Organization

```bash
tests/
├── test_models/           # Model unit tests
├── test_utils/            # Utility unit tests
├── test_integration/      # Integration tests
└── conftest.py           # Shared fixtures
```

## Security Considerations

### 1. File Handling

- Path validation for project files
- Safe deserialization with validation
- Input sanitization for all user data
- Protection against path traversal

### 2. PDF Generation

- Safe text rendering without code execution
- Resource limits for large documents
- Error containment and recovery
- Temporary file cleanup

### 3. User Input

- Validation of all numeric inputs
- Range checking for dimensions
- Type safety with proper conversion
- Sanitization of text content

## Future Architecture Considerations

### 1. Plugin System

- Extensible segment types through plugins
- Custom export formats via plugins
- Third-party integrations
- Plugin discovery and loading

### 2. Multi-Document Support

- Multiple label strips in single project
- Batch processing capabilities
- Template management system
- Project organization features

### 3. Cloud Integration

- Project synchronization across devices
- Collaborative editing capabilities
- Online template sharing
- Backup and versioning

### 4. Advanced Rendering

- 3D preview capabilities
- Print simulation with color management
- Advanced typography features
- Custom font embedding

### 5. Performance Enhancements

- Multi-threaded rendering for large projects
- GPU acceleration for preview rendering
- Incremental updates for better responsiveness
- Background processing for exports

This architecture provides a solid foundation for the current application while maintaining flexibility for future enhancements. The clean separation of concerns, comprehensive error handling, and extensible design patterns ensure the application can evolve to meet changing requirements while maintaining code quality and user experience.
