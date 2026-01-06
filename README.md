# Jackfield Labeler

[![Release](https://img.shields.io/github/v/release/capp3/jackfield-labeler)](https://img.shields.io/github/v/release/capp3/jackfield-labeler)
[![Build status](https://img.shields.io/github/actions/workflow/status/capp3/jackfield-labeler/main.yml?branch=main)](https://github.com/capp3/jackfield-labeler/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/capp3/jackfield-labeler)](https://img.shields.io/github/commit-activity/m/capp3/jackfield-labeler)
[![License](https://img.shields.io/github/license/capp3/jackfield-labeler)](https://img.shields.io/github/license/capp3/jackfield-labeler)

A professional desktop application for creating custom label strips for 19" equipment rack jackfields, patch panels, and audio equipment. Designed for audio engineers, broadcast technicians, IT professionals, and lab managers who need clear, professional labels for their equipment.

- **Github repository**: <https://github.com/capp3/jackfield-labeler/>
- **Documentation**: <https://capp3.github.io/jackfield-labeler/>

## ✨ Features

### 🎨 **Intuitive Label Design**

- **Visual Designer**: Create label strips with customizable segments using an intuitive tabbed interface
- **Real-time Preview**: See your label design update instantly as you make changes
- **Flexible Segments**: Support for start labels, content cells, and end labels with individual customization
- **Rich Text Formatting**: Bold, italic, and normal text options with customizable colors
- **Color Palette**: Comprehensive color selection for text and backgrounds
- **Precise Dimensions**: Exact millimeter precision for professional results

### 📄 **Professional Output**

- **PDF Generation**: High-quality PDF output ready for professional printing
- **PNG Export**: High-resolution PNG export (300 DPI) for digital use
- **Smart Rotation**: Configurable rotation (0°-360°) with 60° default for optimal paper usage
- **Multiple Paper Sizes**: Support for A0-A4, Letter, Legal, and Tabloid paper sizes
- **Center-to-Center Positioning**: Precise positioning algorithm for consistent results
- **No Auto-Scaling**: Preserves exact label dimensions for accurate printing

### 💾 **Project Management**

- **Save/Load Projects**: Save your designs in `.jlp` (Jackfield Labeler Project) format
- **JSON-Based Format**: Human-readable and version-control friendly
- **Project State Tracking**: Visual indicators for unsaved changes
- **Example Projects**: Included sample projects to get you started
- **Metadata Support**: Complete project information and versioning

### ⚙️ **Advanced Settings**

- **Configurable Rotation**: Set custom rotation angles (0°-360°) with 60° default
- **Paper Size Selection**: Choose from standard paper sizes with A3 default
- **Margin Control**: Customizable page margins for optimal printing
- **Font Settings**: Configurable default font and size settings
- **Default Colors**: Set default text and background colors for new segments
- **Logging System**: Configurable logging with multiple levels and optional file output

## 🚀 Quick Start

### Prerequisites

- **Python 3.12 or higher**
- **Operating System**: Windows, macOS, or Linux

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/capp3/jackfield-labeler.git
   cd jackfield-labeler
   ```

2. **Install dependencies using UV:**

   ```bash
   make install
   ```

   Or manually:

   ```bash
   # Install UV if you don't have it
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install dependencies
   uv sync
   ```

3. **Run the application:**

   ```bash
   make run
   ```

   Or directly:

   ```bash
   uv run -m jackfield_labeler
   ```

### First Steps

1. **Open the application** - The Designer tab will be active by default
2. **Set your strip dimensions** - Configure height and segment widths in the control panel
3. **Add content** - Use the segment table to add text, colors, and formatting
4. **Preview your design** - Switch to the Preview tab to see your label
5. **Configure settings** - Use the Settings tab to adjust paper size, rotation, and defaults
6. **Export your label** - Generate PDF or PNG files from the File menu

## 📖 User Guide

### Designer Tab

The Designer tab is your main workspace for creating label strips:

**Control Panel:**

- **Strip Height**: Set the overall height of your label strip (typically 5-12mm)
- **Content Cell Width**: Set uniform width for all content segments
- **End Label Width**: Set width for the end label segment
- **End Label Text**: Text content for the end label
- **Number of Content Cells**: Add or remove content segments

**Segment Table:**

- **Text**: Enter the text for each segment
- **Text Format**: Choose Normal, Bold, or Italic formatting
- **Text Color**: Select text color from the palette
- **Background Color**: Choose background color for each segment

**Actions:**

- **Add Row**: Add new content segments
- **Remove Row**: Delete selected segments
- **Generate PDF**: Create PDF output
- **Save/Load**: Manage your projects

### Preview Tab

The Preview tab shows a real-time visual representation of your label:

- **Strip Information**: Displays dimensions, segment count, and end text
- **Visual Preview**: Scaled preview that updates automatically
- **Export PNG**: Direct PNG export with high resolution (300 DPI)

### Settings Tab

Configure global settings for your labels:

**Paper Settings:**

- **Paper Size**: Choose from A0-A4, Letter, Legal, Tabloid (default: A3)
- **Page Margins**: Set top, right, bottom, left margins

**Rotation Settings:**

- **Rotation Angle**: Set custom rotation (0°-360°, default: 60°)
- **Preset Buttons**: Quick access to common rotations (0°, 90°, 180°, 270°)

**Font Settings:**

- **Default Font**: System font selection
- **Font Size**: Default font size in points
- **Default Colors**: Set default text and background colors

## 🔧 Technical Details

### Architecture

The application follows a clean Model-View-Controller (MVC) architecture:

- **Models** (`jackfield_labeler/models/`): Data structures and business logic
- **Views** (`jackfield_labeler/views/`): PyQt6-based user interface components
- **Utils** (`jackfield_labeler/utils/`): PDF generation, rendering, and project management
- **Controllers** (`jackfield_labeler/controllers/`): Application logic and coordination

### Key Components

- **LabelStrip**: Core data model representing the complete label design
- **Segments**: Individual label segments (Start, Content, End) with properties
- **StripSettings**: Configuration for paper size, margins, rotation, and defaults
- **PDFGenerator**: High-quality PDF output with rotation and positioning
- **StripRenderer**: PNG rendering and preview generation
- **ProjectManager**: Save/load functionality for `.jlp` project files

### Dependencies

**Core Dependencies:**

- **PyQt6** (≥6.9.0): Cross-platform GUI framework
- **ReportLab** (≥4.4.1): Professional PDF generation

**Development Dependencies:**

- **UV**: Modern Python package manager
- **pytest**: Testing framework
- **ruff**: Fast Python linter and formatter (replaces multiple tools including Black)
- **pre-commit**: Git hooks for code quality

### File Format

Projects are saved in `.jlp` (Jackfield Labeler Project) format:

- **JSON-based**: Human-readable and version-control friendly
- **Versioned**: Includes format version for future compatibility
- **Complete**: Stores all label data, settings, and metadata
- **Portable**: Easy to share between users and systems

**Example Structure:**

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

## 📁 Project Structure

```bash
jackfield-labeler/
├── jackfield_labeler/          # Main application package (~3,300 lines)
│   ├── models/                 # Data models and business logic
│   │   ├── label_strip.py      # Core label strip model
│   │   ├── segment_types.py    # Segment implementations
│   │   ├── segment.py          # Base segment class
│   │   ├── strip_settings.py   # Configuration model
│   │   ├── color.py           # Color definitions
│   │   └── text_format.py     # Text formatting enums
│   ├── views/                  # User interface components
│   │   ├── main_window.py      # Main application window
│   │   ├── designer_tab.py     # Label design interface
│   │   ├── preview_tab.py      # Preview and export interface
│   │   └── settings_tab.py     # Settings configuration
│   ├── utils/                  # Utility modules
│   │   ├── pdf_generator.py    # PDF generation engine
│   │   ├── strip_renderer.py   # PNG rendering engine
│   │   ├── project_manager.py  # Project save/load
│   │   └── logger.py           # Logging configuration
│   └── app.py                  # Application entry point
├── docs/                       # Documentation
├── examples/                   # Sample projects
├── tests/                      # Test suite (~350 lines)
└── pyproject.toml             # Project configuration
```

## 🧪 Development

### Setting Up Development Environment

1. **Clone and install:**

   ```bash
   git clone https://github.com/capp3/jackfield-labeler.git
   cd jackfield-labeler
   make install
   ```

2. **Install pre-commit hooks:**

   ```bash
   uv run pre-commit install
   ```

3. **Run tests:**

   ```bash
   make test
   ```

### Development Commands

```bash
# Run the application
make run
uv run -m jackfield_labeler

# Run tests
make test
uv run pytest

# Run linting
make lint
uv run ruff check

# Format code
make format
uv run ruff format

# Build documentation
make docs
uv run mkdocs serve
```

### Adding Dependencies

This project uses UV instead of pip:

```bash
# Add runtime dependency
uv add package-name

# Add development dependency
uv add --group dev package-name

# Update dependencies
uv sync
```

### Code Quality

The project uses Ruff for both linting and formatting:

```bash
# Check code with linter
uv run ruff check

# Format code
uv run ruff format
```

**Code Standards**:

- Follow PEP 8 style guidelines enforced by Ruff
- Use descriptive variable and function names
- Write tests for new functionality
- Update documentation as needed

### CI Workflow

The project uses GitHub Actions for continuous integration:

- **Tests**: Runs the test suite on Python 3.12 and 3.13
- **Linting**: Ensures code quality with Ruff
- **Documentation**: Verifies documentation builds correctly

The release workflow automatically builds binaries for macOS and Windows when a version tag is pushed.

## 📝 Examples

### Basic Label Strip

Create a simple 4-channel audio label:

1. Set strip height to 6mm
2. Set content cell width to 12mm
3. Add 4 content cells with text: "CH1", "CH2", "CH3", "CH4"
4. Choose different background colors for each channel
5. Generate PDF with 60° rotation for A3 paper

### Professional Patch Panel

Create a comprehensive patch panel label:

1. Add start label: "INPUT" (18mm width, blue background, white text, bold)
2. Add 4 content cells for channels (12mm each)
3. Add end label: "OUTPUT" (15mm width, black background, white text, bold)
4. Use color coding: Yellow for line inputs, Red for mic inputs
5. Export as both PDF and PNG for documentation

## ⚙️ Configuration

### Logging System

The application includes a comprehensive logging system to help with troubleshooting and monitoring:

**Configure Logging in Settings Tab:**

1. Open the **Settings** tab
2. Scroll to the **Logging** section
3. Choose your log level:
   - **DEBUG**: Detailed diagnostic information (verbose)
   - **INFO**: General informational messages (default)
   - **WARNING**: Warning messages for potential issues
   - **ERROR**: Error messages for failures
4. Enable **"Save logs to file"** to persist logs to disk
5. Click **"Open Log Folder"** to access log files

**Log File Location:**

Logs are stored in your system's application data directory:
- **macOS**: `~/Library/Application Support/logs/jackfield_labeler.log`
- **Windows**: `%APPDATA%\logs\jackfield_labeler.log`
- **Linux**: `~/.local/share/logs/jackfield_labeler.log`

**Log Features:**

- **Rotating Logs**: Log files automatically rotate at 10MB (keeps 3 backups)
- **Console Output**: Always enabled for immediate feedback
- **Structured Format**: Timestamp, module name, log level, and message
- **Cross-Platform**: "Open Log Folder" button works on all platforms

**What Gets Logged:**

- Application startup and shutdown
- File operations (save/load projects)
- PDF and PNG generation
- Error conditions with full context
- Warning messages for validation issues
- Debug information for troubleshooting

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints throughout
- Write tests for new functionality
- Update documentation as needed
- Use UV for dependency management

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the user interface
- PDF generation powered by [ReportLab](https://www.reportlab.com/)
- Package management by [UV](https://github.com/astral-sh/uv)
- Designed for audio professionals and equipment managers worldwide

---

**Made with ❤️ for the audio and broadcast community**
