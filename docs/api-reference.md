# API Reference

## Overview

This document provides comprehensive API documentation for the Jackfield Labeler application. All public interfaces, classes, and methods are documented with type signatures, parameters, return values, and usage examples.

## Table of Contents

1. [Models Module](#models-module)
2. [Views Module](#views-module)
3. [Utils Module](#utils-module)
4. [Error Handling](#error-handling)
5. [Signals Reference](#signals-reference)
6. [Constants](#constants)
7. [Usage Examples](#usage-examples)

## Models Module

### LabelStrip

The central data model representing a complete label strip design.

```python
class LabelStrip:
    """
    Represents a complete label strip with all its segments.
    
    A label strip consists of:
    - An optional start segment
    - Multiple content segments (cells)
    - An optional end segment
    """
```

#### Constants

```python
MIN_HEIGHT: float = 5.0   # Minimum height in mm
MAX_HEIGHT: float = 12.0  # Maximum height in mm
MAX_WIDTH: float = 500.0  # Maximum total width in mm
```

#### Constructor

```python
def __init__(self, height: float = 5.0) -> None:
    """
    Initialize a new label strip.
    
    Args:
        height: The height of the strip in mm (default: 5.0)
        
    Raises:
        ValueError: If height is outside valid range
    """
```

#### Properties

```python
@property
def height(self) -> float:
    """Get the height of the strip in mm."""

@height.setter
def height(self, value: float) -> None:
    """
    Set the height of the strip in mm.
    
    The height is constrained to the allowed range.
    
    Args:
        value: Height in mm (5.0-12.0)
    """

@property
def content_cell_width(self) -> float:
    """Get the width of content cells in mm."""

@content_cell_width.setter
def content_cell_width(self, value: float) -> None:
    """
    Set the width of content cells in mm.
    
    Args:
        value: Width in mm (must be positive)
        
    Raises:
        ValueError: If the width is negative or zero
    """

@property
def start_segment(self) -> StartSegment | None:
    """Get the start segment, or None if not used."""

@property
def end_segment(self) -> EndSegment | None:
    """Get the end segment, or None if not used."""

@property
def content_segments(self) -> list[ContentSegment]:
    """Get a copy of the list of content segments."""

@property
def settings(self) -> StripSettings:
    """Get the strip settings."""

@settings.setter
def settings(self, value: StripSettings) -> None:
    """Set the strip settings."""
```

#### Methods

```python
def set_start_segment(self, width: float = 0.0, text: str = "") -> StartSegment | None:
    """
    Configure the start segment of the strip.
    
    Args:
        width: Width in mm (0.0 means no start segment)
        text: Text content
        
    Returns:
        The start segment instance, or None if width is 0
        
    Raises:
        ValueError: If the width is negative
    """

def set_end_segment(self, width: float = 0.0, text: str = "") -> EndSegment | None:
    """
    Configure the end segment of the strip.
    
    Args:
        width: Width in mm (0.0 means no end segment)
        text: Text content
        
    Returns:
        The end segment instance, or None if width is 0
        
    Raises:
        ValueError: If the width is negative
    """

def set_content_segment_count(self, count: int) -> None:
    """
    Set the number of content segments.
    
    This will add or remove segments as needed.
    
    Args:
        count: Number of content segments
        
    Raises:
        ValueError: If count is negative
    """

def get_all_segments(self) -> list[Segment]:
    """
    Get all segments in order (start, content, end).
    
    Returns:
        List of all segments in display order
    """

def get_total_width(self) -> float:
    """
    Calculate the total width of the strip.
    
    Returns:
        Total width in mm (sum of all segment widths)
    """

def get_segment_by_id(self, segment_id: str) -> Segment | None:
    """
    Find a segment by its ID.
    
    Args:
        segment_id: The segment identifier
        
    Returns:
        The segment if found, None otherwise
    """

def validate(self) -> list[str]:
    """
    Validate the label strip configuration.
    
    Returns:
        List of validation error messages (empty if valid)
    """

def to_dict(self) -> dict[str, Any]:
    """
    Convert the label strip to a dictionary.
    
    Returns:
        Dictionary representation suitable for JSON serialization
    """

def to_json(self) -> str:
    """
    Convert the label strip to JSON string.
    
    Returns:
        JSON string representation
    """

@classmethod
def from_dict(cls, data: dict[str, Any]) -> "LabelStrip":
    """
    Create a label strip from a dictionary.
    
    Args:
        data: Dictionary containing label strip data
        
    Returns:
        New LabelStrip instance
        
    Raises:
        ValueError: If data is invalid or missing required fields
    """

@classmethod
def from_json(cls, json_str: str) -> "LabelStrip":
    """
    Create a label strip from JSON string.
    
    Args:
        json_str: JSON string containing label strip data
        
    Returns:
        New LabelStrip instance
        
    Raises:
        ValueError: If JSON is invalid or missing required fields
        json.JSONDecodeError: If JSON parsing fails
    """
```

### Segment Classes

#### Base Segment

```python
@dataclass
class Segment:
    """Base class for all segment types."""
    
    width: float
    text: str
    text_color: str
    background_color: str
    text_format: TextFormat
    
    def validate(self) -> list[str]:
        """
        Validate segment properties.
        
        Returns:
            List of validation error messages
        """
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert segment to dictionary.
        
        Returns:
            Dictionary representation
        """
```

#### StartSegment

```python
@dataclass
class StartSegment(Segment):
    """
    Start segment for label strips (e.g., 'INPUT').
    
    Currently not used in the UI but supported in the data model.
    """
    
    def __post_init__(self) -> None:
        """Validate start segment after initialization."""
```

#### ContentSegment

```python
@dataclass
class ContentSegment(Segment):
    """
    Content segment for main label cells (e.g., 'CH1', 'CH2').
    
    These are the primary segments used for channel labeling.
    """
    
    id: str = field(init=False)  # Auto-generated identifier
    
    def __post_init__(self) -> None:
        """Set up content segment after initialization."""
```

#### EndSegment

```python
@dataclass
class EndSegment(Segment):
    """
    End segment for label strips (e.g., 'OUTPUT').
    
    Configurable through the UI with independent width and text.
    """
    
    def __post_init__(self) -> None:
        """Validate end segment after initialization."""
```

#### Factory Function

```python
def create_segment_from_dict(data: dict[str, Any]) -> Segment:
    """
    Create appropriate segment type from dictionary data.
    
    Args:
        data: Dictionary containing segment data with 'type' field
        
    Returns:
        Segment instance of appropriate type
        
    Raises:
        ValueError: If segment type is unknown or data is invalid
    """
```

### StripSettings

Configuration model for global settings.

```python
@dataclass
class StripSettings:
    """Global settings for label strip generation."""
    
    paper_size: str = "A3"
    page_margins: PageMargins = field(default_factory=PageMargins)
    rotation_angle: float = 60.0
    default_font_name: str = "Arial"
    default_font_size: float = 8.0
    default_text_color: str = "#000000"
    default_background_color: str = "#FFFFFF"
```

#### Methods

```python
def validate(self) -> list[str]:
    """
    Validate settings configuration.
    
    Returns:
        List of validation error messages
    """

def to_dict(self) -> dict[str, Any]:
    """
    Convert settings to dictionary.
    
    Returns:
        Dictionary representation
    """

@classmethod
def from_dict(cls, data: dict[str, Any]) -> "StripSettings":
    """
    Create settings from dictionary.
    
    Args:
        data: Dictionary containing settings data
        
    Returns:
        New StripSettings instance
    """
```

### Supporting Classes

#### PageMargins

```python
@dataclass
class PageMargins:
    """Page margin configuration."""
    
    top: float = 10.0
    right: float = 10.0
    bottom: float = 10.0
    left: float = 10.0
    
    def validate(self) -> list[str]:
        """Validate margin values (0-50mm range)."""
```

#### Color

```python
class Color:
    """RGB color representation with standard color constants."""
    
    def __init__(self, red: int, green: int, blue: int) -> None:
        """
        Initialize color with RGB values.
        
        Args:
            red: Red component (0-255)
            green: Green component (0-255)
            blue: Blue component (0-255)
        """
    
    def to_hex(self) -> str:
        """Convert to hex color string (#RRGGBB)."""
    
    def to_rgb_tuple(self) -> tuple[int, int, int]:
        """Convert to RGB tuple."""
    
    @classmethod
    def from_hex(cls, hex_color: str) -> "Color":
        """Create color from hex string."""
    
    # Standard color constants
    BLACK: ClassVar["Color"]
    WHITE: ClassVar["Color"]
    RED: ClassVar["Color"]
    GREEN: ClassVar["Color"]
    BLUE: ClassVar["Color"]
    YELLOW: ClassVar["Color"]
    ORANGE: ClassVar["Color"]
    PURPLE: ClassVar["Color"]
```

#### TextFormat

```python
class TextFormat(Enum):
    """Text formatting options."""
    
    NORMAL = "NORMAL"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
```

#### PaperSize

```python
class PaperSize(Enum):
    """Standard paper sizes with dimensions in mm."""
    
    A0 = "A0"      # 841 × 1189 mm
    A1 = "A1"      # 594 × 841 mm
    A2 = "A2"      # 420 × 594 mm
    A3 = "A3"      # 297 × 420 mm
    A4 = "A4"      # 210 × 297 mm
    LETTER = "Letter"    # 216 × 279 mm
    LEGAL = "Legal"      # 216 × 356 mm
    TABLOID = "Tabloid"  # 279 × 432 mm
```

## Views Module

### MainWindow

The primary application window that coordinates all functionality.

```python
class MainWindow(QMainWindow):
    """Main application window with tab management and file operations."""
```

#### Signals

```python
project_changed = pyqtSignal()  # Emitted when project state changes
file_saved = pyqtSignal(str)    # Emitted when file is saved (filename)
file_loaded = pyqtSignal(str)   # Emitted when file is loaded (filename)
```

#### Constructor

```python
def __init__(self) -> None:
    """Initialize the main window with tabs and menu bar."""
```

#### Methods

```python
def new_project(self) -> None:
    """Create a new project, prompting to save current changes."""

def open_project(self) -> None:
    """Open an existing project file."""

def save_project(self) -> None:
    """Save the current project."""

def save_project_as(self) -> None:
    """Save the current project with a new filename."""

def generate_pdf(self) -> None:
    """Generate PDF output of the current label strip."""

def export_png(self) -> None:
    """Export PNG image of the current label strip."""

def get_current_label_strip(self) -> LabelStrip:
    """Get the current label strip from the designer tab."""

def set_project_modified(self, modified: bool) -> None:
    """Update the project modification state."""

def closeEvent(self, event: QCloseEvent) -> None:
    """Handle window close event with save prompt."""
```

### DesignerTab

Main workspace for creating and editing label strips.

```python
class DesignerTab(QWidget):
    """Label design interface with control panel and segment table."""
```

#### Signals

```python
strip_changed = pyqtSignal()           # Emitted when strip is modified
segment_added = pyqtSignal(int)        # Emitted when segment is added
segment_removed = pyqtSignal(int)      # Emitted when segment is removed
```

#### Constructor

```python
def __init__(self) -> None:
    """Initialize the designer tab with control panel and table."""
```

#### Methods

```python
def get_label_strip(self) -> LabelStrip:
    """Get the current label strip configuration."""

def set_label_strip(self, label_strip: LabelStrip) -> None:
    """Set the label strip configuration and update UI."""

def add_content_segment(self) -> None:
    """Add a new content segment to the table."""

def remove_selected_segment(self) -> None:
    """Remove the currently selected segment."""

def apply_settings(self, settings: StripSettings) -> None:
    """Apply global settings to the current strip."""

def validate_input(self) -> list[str]:
    """Validate all user input and return error messages."""
```

### PreviewTab

Real-time visual preview and PNG export functionality.

```python
class PreviewTab(QWidget):
    """Preview interface with visual representation and export controls."""
```

#### Constructor

```python
def __init__(self) -> None:
    """Initialize the preview tab with preview widget and controls."""
```

#### Methods

```python
def update_preview(self, label_strip: LabelStrip) -> None:
    """Update the preview with the given label strip."""

def export_png(self, filename: str) -> bool:
    """
    Export the current preview as PNG.
    
    Args:
        filename: Output filename
        
    Returns:
        True if export successful, False otherwise
    """

def get_preview_scale_factor(self) -> float:
    """Get the current preview scale factor."""

def refresh_preview(self) -> None:
    """Force refresh of the preview display."""
```

### SettingsTab

Global configuration interface for paper, rotation, and default settings.

```python
class SettingsTab(QWidget):
    """Settings interface with grouped configuration controls."""
```

#### Signals

```python
settings_changed = pyqtSignal(StripSettings)  # Emitted when settings change
```

#### Constructor

```python
def __init__(self) -> None:
    """Initialize the settings tab with grouped controls."""
```

#### Methods

```python
def get_settings(self) -> StripSettings:
    """Get the current settings configuration."""

def set_settings(self, settings: StripSettings) -> None:
    """Set the settings configuration and update UI."""

def reset_to_defaults(self) -> None:
    """Reset all settings to default values."""

def validate_settings(self) -> list[str]:
    """Validate current settings and return error messages."""
```

## Utils Module

### PDFGenerator

High-quality PDF generation with rotation and positioning.

```python
class PDFGenerator:
    """Professional PDF generation using ReportLab."""
```

#### Constructor

```python
def __init__(self) -> None:
    """Initialize the PDF generator with default settings."""
```

#### Methods

```python
def generate_pdf(
    self,
    label_strip: LabelStrip,
    filename: str,
    settings: StripSettings | None = None
) -> bool:
    """
    Generate PDF file from label strip.
    
    Args:
        label_strip: The label strip to render
        filename: Output PDF filename
        settings: Optional settings override
        
    Returns:
        True if generation successful, False otherwise
        
    Raises:
        IOError: If file cannot be written
        ValueError: If label strip is invalid
    """

def calculate_positioning(
    self,
    strip_width: float,
    strip_height: float,
    paper_size: str,
    rotation_angle: float
) -> tuple[float, float]:
    """
    Calculate center positioning for strip on paper.
    
    Args:
        strip_width: Width of strip in mm
        strip_height: Height of strip in mm
        paper_size: Paper size identifier
        rotation_angle: Rotation angle in degrees
        
    Returns:
        Tuple of (center_x, center_y) in points
    """

def get_paper_dimensions(self, paper_size: str) -> tuple[float, float]:
    """
    Get paper dimensions in points.
    
    Args:
        paper_size: Paper size identifier
        
    Returns:
        Tuple of (width, height) in points
        
    Raises:
        ValueError: If paper size is not supported
    """
```

### StripRenderer

PNG rendering and preview generation engine.

```python
class StripRenderer:
    """High-quality PNG rendering using Qt."""
```

#### Constructor

```python
def __init__(self, dpi: int = 300) -> None:
    """
    Initialize the renderer.
    
    Args:
        dpi: Dots per inch for output resolution
    """
```

#### Methods

```python
def render_to_pixmap(
    self,
    label_strip: LabelStrip,
    scale_factor: float = 1.0
) -> QPixmap:
    """
    Render label strip to QPixmap.
    
    Args:
        label_strip: The label strip to render
        scale_factor: Scale factor for output size
        
    Returns:
        QPixmap containing rendered strip
    """

def render_to_file(
    self,
    label_strip: LabelStrip,
    filename: str,
    dpi: int | None = None
) -> bool:
    """
    Render label strip directly to PNG file.
    
    Args:
        label_strip: The label strip to render
        filename: Output PNG filename
        dpi: Optional DPI override
        
    Returns:
        True if rendering successful, False otherwise
    """

def calculate_dimensions(
    self,
    label_strip: LabelStrip,
    scale_factor: float = 1.0
) -> tuple[int, int]:
    """
    Calculate pixel dimensions for rendering.
    
    Args:
        label_strip: The label strip
        scale_factor: Scale factor
        
    Returns:
        Tuple of (width_px, height_px)
    """
```

### ProjectManager

Project file management with .jlp format support.

```python
class ProjectManager:
    """Project file management and serialization."""
```

#### Static Methods

```python
@staticmethod
def save_project(label_strip: LabelStrip, filename: str) -> bool:
    """
    Save project to .jlp file.
    
    Args:
        label_strip: The label strip to save
        filename: Output filename
        
    Returns:
        True if save successful, False otherwise
        
    Raises:
        IOError: If file cannot be written
        ValueError: If label strip is invalid
    """

@staticmethod
def load_project(filename: str) -> LabelStrip:
    """
    Load project from .jlp file.
    
    Args:
        filename: Input filename
        
    Returns:
        Loaded LabelStrip instance
        
    Raises:
        IOError: If file cannot be read
        ValueError: If file format is invalid
        json.JSONDecodeError: If JSON parsing fails
    """

@staticmethod
def validate_project_file(filename: str) -> bool:
    """
    Validate project file format.
    
    Args:
        filename: File to validate
        
    Returns:
        True if file is valid, False otherwise
    """

@staticmethod
def get_project_metadata(filename: str) -> dict[str, Any]:
    """
    Extract metadata from project file.
    
    Args:
        filename: Project file
        
    Returns:
        Dictionary containing metadata
        
    Raises:
        IOError: If file cannot be read
        ValueError: If file format is invalid
    """
```

## Error Handling

### Exception Hierarchy

```python
class JackfieldLabelerError(Exception):
    """Base exception for all application errors."""

class ValidationError(JackfieldLabelerError):
    """Raised when validation fails."""

class FileFormatError(JackfieldLabelerError):
    """Raised when file format is invalid."""

class RenderingError(JackfieldLabelerError):
    """Raised when rendering fails."""

class ConfigurationError(JackfieldLabelerError):
    """Raised when configuration is invalid."""
```

### Error Handling Patterns

```python
# Model validation
try:
    errors = label_strip.validate()
    if errors:
        raise ValidationError(f"Validation failed: {', '.join(errors)}")
except ValidationError as e:
    # Handle validation errors
    show_error_message(str(e))

# File operations
try:
    label_strip = ProjectManager.load_project(filename)
except (IOError, FileFormatError) as e:
    # Handle file errors
    show_error_message(f"Failed to load project: {e}")

# PDF generation
try:
    success = pdf_generator.generate_pdf(label_strip, filename)
    if not success:
        raise RenderingError("PDF generation failed")
except RenderingError as e:
    # Handle rendering errors
    show_error_message(str(e))
```

## Signals Reference

### Model Signals

```python
# LabelStrip signals (if QObject-based)
strip_changed = pyqtSignal()                    # Strip modified
segment_added = pyqtSignal(int)                 # Segment added (index)
segment_removed = pyqtSignal(int)               # Segment removed (index)
settings_changed = pyqtSignal(StripSettings)    # Settings modified
```

### View Signals

```python
# MainWindow signals
project_changed = pyqtSignal()                  # Project state changed
file_saved = pyqtSignal(str)                    # File saved (filename)
file_loaded = pyqtSignal(str)                   # File loaded (filename)

# DesignerTab signals
strip_changed = pyqtSignal()                    # Strip design changed
segment_added = pyqtSignal(int)                 # Segment added
segment_removed = pyqtSignal(int)               # Segment removed

# SettingsTab signals
settings_changed = pyqtSignal(StripSettings)    # Settings changed

# PreviewTab signals
preview_updated = pyqtSignal()                  # Preview refreshed
export_completed = pyqtSignal(str)              # Export completed (filename)
```

### Signal Connection Examples

```python
# Connect designer changes to preview updates
designer_tab.strip_changed.connect(preview_tab.update_preview)

# Connect settings changes to designer
settings_tab.settings_changed.connect(designer_tab.apply_settings)

# Connect file operations
main_window.file_saved.connect(lambda f: status_bar.showMessage(f"Saved: {f}"))
main_window.file_loaded.connect(lambda f: status_bar.showMessage(f"Loaded: {f}"))
```

## Constants

### Application Constants

```python
# Application information
APP_NAME = "Jackfield Labeler"
APP_VERSION = "1.0.0"
FILE_FORMAT_VERSION = "1.0"

# File extensions
PROJECT_EXTENSION = ".jlp"
PDF_EXTENSION = ".pdf"
PNG_EXTENSION = ".png"

# Default values
DEFAULT_STRIP_HEIGHT = 6.0          # mm
DEFAULT_CONTENT_WIDTH = 12.0        # mm
DEFAULT_ROTATION_ANGLE = 60.0       # degrees
DEFAULT_PAPER_SIZE = "A3"
DEFAULT_FONT_NAME = "Arial"
DEFAULT_FONT_SIZE = 8.0             # points
DEFAULT_DPI = 300                   # dots per inch

# Validation limits
MIN_STRIP_HEIGHT = 5.0              # mm
MAX_STRIP_HEIGHT = 12.0             # mm
MAX_TOTAL_WIDTH = 500.0             # mm
MIN_SEGMENT_WIDTH = 0.1             # mm
MAX_MARGIN = 50.0                   # mm

# Color constants (hex strings)
DEFAULT_TEXT_COLOR = "#000000"      # Black
DEFAULT_BACKGROUND_COLOR = "#FFFFFF" # White
```

### Paper Size Constants

```python
PAPER_SIZES = {
    "A0": (841, 1189),      # mm
    "A1": (594, 841),       # mm
    "A2": (420, 594),       # mm
    "A3": (297, 420),       # mm
    "A4": (210, 297),       # mm
    "Letter": (216, 279),   # mm
    "Legal": (216, 356),    # mm
    "Tabloid": (279, 432),  # mm
}

# Points per mm conversion
POINTS_PER_MM = 2.834645669
```

## Usage Examples

### Creating a Label Strip

```python
from jackfield_labeler.models import LabelStrip, StripSettings

# Create a new label strip
strip = LabelStrip(height=6.0)

# Set content cell width
strip.content_cell_width = 12.0

# Add content segments
strip.set_content_segment_count(4)

# Configure segments
segments = strip.content_segments
segments[0].text = "CH1"
segments[0].background_color = "#FFFF00"  # Yellow
segments[1].text = "CH2"
segments[1].background_color = "#FF0000"  # Red
segments[2].text = "CH3"
segments[2].background_color = "#00FF00"  # Green
segments[3].text = "CH4"
segments[3].background_color = "#0000FF"  # Blue

# Add end segment
strip.set_end_segment(width=15.0, text="OUTPUT")

# Validate the strip
errors = strip.validate()
if errors:
    print(f"Validation errors: {errors}")
else:
    print(f"Strip is valid, total width: {strip.get_total_width()}mm")
```

### Generating PDF Output

```python
from jackfield_labeler.utils import PDFGenerator
from jackfield_labeler.models import StripSettings

# Create PDF generator
generator = PDFGenerator()

# Configure settings
settings = StripSettings(
    paper_size="A3",
    rotation_angle=60.0
)

# Generate PDF
success = generator.generate_pdf(
    label_strip=strip,
    filename="my_label.pdf",
    settings=settings
)

if success:
    print("PDF generated successfully")
else:
    print("PDF generation failed")
```

### Rendering PNG Image

```python
from jackfield_labeler.utils import StripRenderer

# Create renderer with high DPI
renderer = StripRenderer(dpi=300)

# Render to file
success = renderer.render_to_file(
    label_strip=strip,
    filename="my_label.png"
)

if success:
    print("PNG exported successfully")
else:
    print("PNG export failed")
```

### Project File Management

```python
from jackfield_labeler.utils import ProjectManager

# Save project
success = ProjectManager.save_project(strip, "my_project.jlp")
if success:
    print("Project saved")

# Load project
try:
    loaded_strip = ProjectManager.load_project("my_project.jlp")
    print(f"Loaded strip with {len(loaded_strip.content_segments)} segments")
except (IOError, ValueError) as e:
    print(f"Failed to load project: {e}")

# Validate project file
if ProjectManager.validate_project_file("my_project.jlp"):
    print("Project file is valid")
else:
    print("Project file is invalid")
```

### Working with Colors

```python
from jackfield_labeler.models import Color

# Create colors
red = Color(255, 0, 0)
blue = Color.from_hex("#0000FF")

# Use standard colors
yellow = Color.YELLOW
green = Color.GREEN

# Convert colors
hex_color = red.to_hex()        # "#FF0000"
rgb_tuple = blue.to_rgb_tuple() # (0, 0, 255)

# Apply to segments
segment.text_color = red.to_hex()
segment.background_color = yellow.to_hex()
```

### Custom Validation

```python
def validate_professional_strip(strip: LabelStrip) -> list[str]:
    """Custom validation for professional use."""
    errors = []
    
    # Check minimum dimensions
    if strip.height < 6.0:
        errors.append("Professional strips should be at least 6mm high")
    
    # Check segment count
    if len(strip.content_segments) < 2:
        errors.append("Professional strips should have at least 2 channels")
    
    # Check text content
    for i, segment in enumerate(strip.content_segments):
        if not segment.text.strip():
            errors.append(f"Segment {i+1} has no text")
    
    return errors

# Use custom validation
errors = validate_professional_strip(strip)
if errors:
    print("Professional validation failed:")
    for error in errors:
        print(f"  - {error}")
```

This API reference provides comprehensive documentation for all public interfaces in the Jackfield Labeler application. For additional examples and usage patterns, refer to the test suite and user guide documentation.
