# User Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Application Overview](#application-overview)
3. [Designer Tab](#designer-tab)
4. [Preview Tab](#preview-tab)
5. [Settings Tab](#settings-tab)
6. [File Operations](#file-operations)
7. [Export Options](#export-options)
8. [Tips and Best Practices](#tips-and-best-practices)
9. [Troubleshooting](#troubleshooting)

## Getting Started

### First Launch

When you first launch Jackfield Labeler, you'll see the main window with three tabs:

- **Designer**: Where you create your label strips
- **Preview**: Where you see a visual representation of your label
- **Settings**: Where you configure global settings

The application starts with a default label strip configuration that you can immediately modify.

### Quick Start Tutorial

Let's create your first label strip:

1. **Set Strip Dimensions**
   - In the Designer tab, set "Strip Height" to `6.0` mm
   - Set "Content Cell Width" to `12.0` mm
   - Set "Number of Content Cells" to `4`

2. **Add Content**
   - In the segment table, enter text for each cell: "CH1", "CH2", "CH3", "CH4"
   - Choose different background colors for each channel
   - Keep text color as black for readability

3. **Preview Your Design**
   - Click the "Preview" tab to see your label
   - The preview updates automatically as you make changes

4. **Generate PDF**
   - Go to File → Generate PDF or click the "Generate PDF" button
   - Choose a location to save your PDF
   - Your label will be generated with the current settings

## Application Overview

### Main Window Components

- **Menu Bar**: File operations, export options, and help
- **Tab Widget**: Three main tabs for different functions
- **Status Bar**: Shows current operation status and feedback
- **Window Title**: Displays current project name and modification status

### Keyboard Shortcuts

- **Ctrl+N**: New project
- **Ctrl+O**: Open project
- **Ctrl+S**: Save project
- **Ctrl+Shift+S**: Save project as
- **F5**: Generate PDF
- **F6**: Export PNG

### Project State Tracking

The application tracks your project state:

- **Window Title**: Shows project name with "*" for unsaved changes
- **Status Messages**: Confirmation and error messages
- **Auto-Save Prompts**: Warns before losing unsaved work

## Designer Tab

The Designer tab is your main workspace for creating label strips.

### Control Panel

Located at the top of the Designer tab, the control panel contains global settings for your label strip:

#### Strip Dimensions

- **Strip Height (mm)**: The overall height of your label strip
  - Typical values: 5-12mm for jackfield labels
  - Supports one decimal place (e.g., 6.5mm)
  - Range: 5.0mm to 12.0mm (enforced by validation)
  - Default: 5.0mm

- **Content Cell Width (mm)**: Uniform width for all content segments
  - Typical values: 8-15mm depending on text length
  - Supports three decimal places for precision
  - Range: Must be positive (no upper limit)
  - Default: 10.0mm

- **End Label Width (mm)**: Width of the optional end label
  - Set to 0 to disable the end label
  - Supports three decimal places
  - Range: 0.0mm or positive values
  - Default: 0.0mm (disabled)

#### Content Management

- **Number of Content Cells**: How many main content segments to create
  - Range: 0 to unlimited (practical limit ~50 for usability)
  - Use spin box controls or type directly
  - Changes are applied immediately
  - Default: 0 (empty strip)

- **End Label Text**: Text for the end label segment
  - Only visible when End Label Width > 0
  - Supports all text formatting options
  - Updates the end segment automatically
  - Default: Empty string

#### Display Information

- **Total Strip Width**: Automatically calculated and displayed
  - Shows the sum of all segment widths
  - Updates in real-time as you change dimensions
  - Helps you plan for paper size requirements
  - Maximum total width: 500.0mm

### Segment Table

The segment table provides a spreadsheet-like interface for editing individual segments:

#### Table Columns

1. **Segment**: Read-only identifier
   - Content segments numbered 1, 2, 3, etc.
   - End segment labeled "L_END" (when present)
   - Cannot be edited directly

2. **Text**: The text to display on each segment
   - Click to edit directly
   - Supports Unicode characters
   - No length limit, but consider readability
   - Empty text is allowed

3. **Text Format**: Formatting options for the text
   - **Normal**: Standard text (default)
   - **Bold**: Bold text for emphasis
   - **Italic**: Italic text for style
   - Choose from dropdown menu

4. **Text Color**: Color of the text
   - Click the color button to open color picker
   - Standard colors: Black, White, Red, Green, Blue, Yellow, Orange, Purple
   - Custom colors available through color dialog
   - Default: Black (#000000)

5. **Background Color**: Background color of the segment
   - Click the color button to open color picker
   - Same color options as text color
   - Consider contrast with text color for readability
   - Default: White (#FFFFFF)

#### Table Operations

- **Add Row**: Click "Add Row" button to add new content segments
- **Remove Row**: Select a row and click "Remove Row" to delete it
- **Direct Editing**: Click any cell to edit its value
- **Tab Navigation**: Use Tab key to move between cells
- **Enter Confirmation**: Press Enter to confirm changes
- **Color Picker**: Click color buttons to open color selection dialog

#### Table Behavior

- **Real-time Updates**: Changes are applied immediately
- **Validation**: Invalid inputs are highlighted and prevented
- **Auto-Resize**: Table adjusts to content automatically
- **Selection**: Single row selection for operations

### Action Buttons

Located at the bottom of the Designer tab:

- **Add Row**: Adds a new content segment to the table
  - Uses default colors from settings
  - Increments segment numbering automatically
  - Updates total width calculation

- **Remove Row**: Removes the selected segment from the table
  - Requires a row to be selected
  - Cannot remove if no segments exist
  - Updates segment numbering automatically

- **Generate PDF**: Creates a PDF file of your label strip
  - Uses current settings for paper size and rotation
  - Opens file dialog for save location
  - Shows progress and confirmation messages

- **Save**: Saves your current project
  - Uses existing filename or prompts for new one
  - Saves in .jlp format with all settings
  - Updates window title and project state

- **Load**: Loads a previously saved project
  - Opens file dialog for .jlp files
  - Validates file format before loading
  - Prompts to save current project if modified

## Preview Tab

The Preview tab provides real-time visualization of your label strip design.

### Strip Information Panel

Located at the top of the Preview tab, this panel shows:

- **Dimensions**: Current strip width × height in millimeters
  - Format: "XXX.X × XX.X mm"
  - Updates automatically when strip changes
  - Helps verify dimensions before printing

- **Segments**: Total number of segments in your strip
  - Includes content segments and end segment (if present)
  - Does not include start segment (not currently used)
  - Format: "X segments"

- **End Text**: Text of the end label (if present)
  - Shows actual text content
  - Only displayed when end segment exists
  - Format: "End: 'TEXT'"

### Visual Preview

The main preview area shows a scaled representation of your label:

#### Preview Features

- **Auto-scaling**: Automatically scales to fit the available space
- **Real-time Updates**: Changes immediately when you modify the design
- **Scrollable**: Use scroll bars for very large labels
- **Responsive**: Adapts to window resizing
- **High Quality**: Anti-aliased rendering for smooth appearance

#### Preview Rendering

- **Scale Calculation**: Automatically determines best fit
- **Aspect Ratio**: Maintains correct proportions
- **Color Accuracy**: Shows actual colors as they will appear
- **Text Rendering**: Shows actual fonts and formatting

#### Preview Controls

- **Zoom**: The preview automatically calculates the best zoom level
- **Scroll**: Use scroll bars to navigate large labels that exceed window size
- **Resize**: Resize the window to see different scale factors
- **Refresh**: Preview updates automatically, no manual refresh needed

### Export Controls

- **Export PNG**: Creates a high-resolution PNG file
  - Fixed at 300 DPI for professional quality
  - No rotation applied - exact strip dimensions
  - Suitable for digital documentation
  - Opens file dialog for save location

#### PNG Export Features

- **High Resolution**: 300 DPI for print quality
- **Exact Dimensions**: No scaling or rotation applied
- **Transparency**: White background for easy integration
- **Color Accuracy**: Maintains exact colors from design

## Settings Tab

The Settings tab configures global options that affect all label generation.

### Paper Settings

#### Paper Size

Choose from standard paper sizes:

- **A0**: 841 × 1189 mm (largest)
- **A1**: 594 × 841 mm
- **A2**: 420 × 594 mm
- **A3**: 297 × 420 mm (default)
- **A4**: 210 × 297 mm
- **Letter**: 216 × 279 mm
- **Legal**: 216 × 356 mm
- **Tabloid**: 279 × 432 mm

**Selection Guidelines:**

- **A3**: Best for most jackfield labels (default)
- **A4**: For smaller labels or when A3 not available
- **Larger sizes**: For very long strips or multiple strips per page

#### Page Margins

Set margins for PDF output:

- **Top**: Space from top edge of paper
- **Right**: Space from right edge of paper
- **Bottom**: Space from bottom edge of paper
- **Left**: Space from left edge of paper
- **Default**: 10mm on all sides
- **Range**: 0-50mm per margin
- **Units**: Millimeters

**Margin Guidelines:**

- **10mm**: Standard for most printers
- **5mm**: Minimum for most printers
- **15-20mm**: Conservative for older printers
- **0mm**: Only if printer supports borderless printing

### Rotation Settings

#### Rotation Angle

- **Custom Angle**: Set any angle from -360° to +360°
- **Default**: 60° (optimized for long strips on A3 paper)
- **Precision**: Supports decimal degrees
- **Input**: Spin box or direct text entry

**Rotation Guidelines:**

- **0°**: Horizontal orientation (no rotation)
- **60°**: Optimal for long strips on A3 paper
- **90°**: Vertical orientation
- **45°**: Diagonal for maximum length

#### Preset Buttons

Quick access to common rotations:

- **0°**: No rotation (horizontal)
- **90°**: Quarter turn (vertical)
- **180°**: Half turn (upside down)
- **270°**: Three-quarter turn

**When to Use Presets:**

- **0°**: Short strips that fit horizontally
- **90°**: When you want vertical orientation
- **180°**: Special cases or testing
- **270°**: Alternative vertical orientation

### Font Settings

#### Default Font

- **Font Family**: Choose from system fonts
- **Font Size**: Default size in points (typical: 8-12pt)
- **Preview**: Shows sample text with selected font
- **System Fonts**: Uses fonts installed on your system

**Font Selection:**

- **Arial**: Good general-purpose font (default)
- **Helvetica**: Clean, professional appearance
- **Times**: Traditional serif font
- **Courier**: Monospace for technical labels

#### Font Configuration

- Click "Select Font" to open font dialog
- Preview shows how text will appear
- Changes apply to new segments only
- Existing segments retain their current formatting

### Default Colors

#### Default Text Color

- Sets the text color for new segments
- Existing segments are not changed
- Choose from standard palette or custom colors
- Default: Black (#000000)

**Text Color Guidelines:**

- **Black**: Maximum readability on light backgrounds
- **White**: For dark backgrounds
- **Dark colors**: Generally better for readability
- **Bright colors**: Use sparingly for emphasis

#### Default Background Color

- Sets the background color for new segments
- Existing segments are not changed
- Consider contrast with text color
- Default: White (#FFFFFF)

**Background Color Guidelines:**

- **White**: Clean, professional appearance
- **Light colors**: Good for color coding
- **Dark colors**: Use with white or light text
- **High contrast**: Essential for readability

### Settings Application

- **Immediate Effect**: Most settings apply immediately
- **New Segments**: Color and font defaults affect new segments only
- **Global Settings**: Paper size, margins, and rotation affect all output
- **Persistence**: Settings are saved with your project

## File Operations

### Project Management

#### New Project

- **Menu**: File → New
- **Shortcut**: Ctrl+N
- **Action**: Creates a fresh label strip with default settings
- **Warning**: Prompts to save unsaved changes
- **Result**: Empty strip ready for design

#### Open Project

- **Menu**: File → Open
- **Shortcut**: Ctrl+O
- **File Type**: `.jlp` (Jackfield Labeler Project) files
- **Action**: Loads a previously saved project
- **Warning**: Prompts to save unsaved changes
- **Validation**: Checks file format before loading

#### Save Project

- **Menu**: File → Save
- **Shortcut**: Ctrl+S
- **Action**: Saves to current file or prompts for new file
- **Format**: JSON-based `.jlp` format
- **Content**: Complete project including settings

#### Save Project As

- **Menu**: File → Save As
- **Shortcut**: Ctrl+Shift+S
- **Action**: Always prompts for new file location
- **Use Case**: Creating copies or renaming projects
- **Result**: New file created, becomes current project

### Project File Format

Jackfield Labeler uses `.jlp` files with the following features:

#### File Structure

```json
{
  "version": "1.0",
  "application": "Jackfield Labeler",
  "label_strip": {
    "height": 6.0,
    "content_cell_width": 12.0,
    "segments": [
      {
        "type": "content",
        "id": "1",
        "width": 12.0,
        "text": "CH1",
        "text_color": "#000000",
        "background_color": "#FFFF00",
        "text_format": "NORMAL"
      }
    ],
    "settings": {
      "paper_size": "A3",
      "rotation_angle": 60.0,
      "default_font_name": "Arial",
      "default_font_size": 8.0
    }
  },
  "metadata": {
    "created_by": "Jackfield Labeler",
    "file_format_version": "1.0"
  }
}
```

#### Benefits

- **Human-readable**: JSON format for easy inspection
- **Version control**: Works well with Git and other VCS
- **Portable**: Share projects between users and systems
- **Future-proof**: Versioned format for compatibility
- **Editable**: Can be modified with text editors if needed

### Project State Tracking

The application tracks your project state:

#### Window Title

- Shows current project name
- Displays "*" for unsaved changes
- Updates automatically
- Format: "Jackfield Labeler - [project.jlp]*"

#### Status Messages

- Confirmation when files are saved
- Error messages for file problems
- Progress updates for long operations
- User feedback for all operations

#### File Validation

- Checks file format before loading
- Validates JSON structure
- Verifies required fields
- Provides helpful error messages

## Export Options

### PDF Generation

#### Access Methods

- **Menu**: File → Generate PDF
- **Button**: "Generate PDF" in Designer tab
- **Shortcut**: F5

#### PDF Features

- **High Quality**: Vector-based output for crisp printing
- **Exact Dimensions**: No scaling - preserves precise measurements
- **Smart Rotation**: Uses rotation angle from settings
- **Professional Output**: Ready for commercial printing
- **Center Positioning**: Optimal placement on paper

#### PDF Process

1. Click Generate PDF
2. Choose file location and name
3. PDF is created with current settings
4. Confirmation message shows success
5. File is ready for printing

#### PDF Technical Details

- **Format**: Standard PDF 1.4
- **Resolution**: Vector-based (infinite resolution)
- **Colors**: RGB color space
- **Fonts**: Embedded for consistency
- **Size**: Typically 1-5KB for most labels

### PNG Export

#### Access Methods

- **Menu**: File → Export PNG
- **Button**: "Export PNG" in Preview tab
- **Shortcut**: F6

#### PNG Features

- **High Resolution**: 300 DPI for professional quality
- **No Rotation**: Exact strip dimensions
- **Digital Use**: Perfect for documentation and digital sharing
- **Transparency**: White background for easy integration
- **Color Accuracy**: Maintains exact colors from design

#### PNG Process

1. Click Export PNG
2. Choose file location and name
3. PNG is created at 300 DPI
4. Confirmation message shows success
5. File is ready for digital use

#### PNG Technical Details

- **Resolution**: 300 DPI (dots per inch)
- **Color Depth**: 24-bit RGB
- **Compression**: PNG lossless compression
- **Background**: Solid white
- **Size**: Varies with dimensions (typically 50-500KB)

### Output Considerations

#### Choosing PDF vs PNG

- **PDF**: For printing, exact dimensions, rotation needed
- **PNG**: For digital use, documentation, no rotation
- **Both**: Create both for complete documentation

#### Quality Settings

- **PDF**: Vector-based, scales to any size
- **PNG**: 300 DPI raster, fixed resolution
- **Print Quality**: Both suitable for professional printing

#### File Sizes

- **PDF**: Small file size, typically 1-5KB
- **PNG**: Larger file size, depends on dimensions and DPI
- **Storage**: PDF more efficient for archival

## Tips and Best Practices

### Design Guidelines

#### Text Readability

- Use high contrast between text and background colors
- Choose appropriate font sizes (8-12pt typical)
- Avoid very long text in narrow segments
- Test readability at actual print size
- Consider viewing distance when choosing font size

#### Color Selection

- **Black on White**: Maximum readability
- **White on Dark**: Good for emphasis
- **Color Coding**: Use consistent colors for similar functions
- **Print Considerations**: Some colors may not print as expected
- **Accessibility**: Consider color-blind users

#### Dimensions

- **Standard Heights**: 5-12mm for most jackfield applications
- **Content Width**: 8-15mm depending on text length
- **Total Width**: Consider your paper size and rotation
- **Precision**: Use decimal places for exact measurements
- **Practical Limits**: Very small text may be unreadable

### Workflow Optimization

#### Project Organization

- Save projects with descriptive names
- Use folders to organize related projects
- Include version numbers for iterative designs
- Document your color coding schemes
- Create templates for common layouts

#### Efficient Design Process

1. Start with dimensions and basic layout
2. Add all text content first
3. Apply formatting and colors
4. Preview frequently during design
5. Test print on draft paper before final output

#### Template Creation

- Create base projects for common layouts
- Save with standard dimensions and colors
- Use as starting points for new projects
- Share templates with team members
- Document template usage guidelines

### Printing Tips

#### Paper Selection

- Use high-quality paper for professional results
- Consider adhesive-backed paper for labels
- Test print settings with your specific printer
- Verify colors match your design intent
- Choose appropriate paper weight

#### Print Settings

- Use highest quality print settings
- Ensure "Fit to Page" is disabled
- Check that rotation is handled correctly
- Verify margins don't clip your design
- Test with draft prints first

#### Cutting and Application

- Use a sharp blade for clean cuts
- Consider adding cut marks for guidance
- Test adhesion on your target surface
- Allow for slight misalignment in application
- Plan for environmental conditions

### Color Management

#### Color Consistency

- Use standard colors when possible
- Test print colors before final production
- Consider printer color profiles
- Document color choices for consistency
- Use color swatches for reference

#### Accessibility

- Ensure sufficient contrast ratios
- Test with color-blind simulation tools
- Provide alternative identification methods
- Consider monochrome printing compatibility
- Follow accessibility guidelines

## Troubleshooting

### Common Issues

#### Application Won't Start

**Problem**: Application fails to launch

**Solutions**:

- Verify Python 3.12+ is installed
- Check that PyQt6 is properly installed
- Run `uv run -m jackfield_labeler` from command line
- Check for error messages in terminal
- Verify UV is installed and working

**Diagnostic Steps**:

```bash
# Check Python version
python --version

# Check UV installation
uv --version

# Try running directly
uv run -m jackfield_labeler

# Check dependencies
uv pip list
```

#### PDF Generation Fails

**Problem**: PDF export produces errors

**Solutions**:

- Verify all text fields are valid
- Check that strip dimensions are reasonable
- Ensure output directory is writable
- Try a different file name/location
- Check available disk space

**Common Causes**:

- Invalid characters in filename
- Insufficient permissions
- Very large strip dimensions
- Corrupted project data

#### Preview Not Updating

**Problem**: Preview tab doesn't show changes

**Solutions**:

- Switch to another tab and back
- Check that segments have valid dimensions
- Verify text and colors are properly set
- Restart the application if needed
- Check for error messages

**Diagnostic Steps**:

1. Verify strip has content
2. Check total width calculation
3. Look for validation errors
4. Try creating new project

#### Colors Look Wrong

**Problem**: Colors in output don't match preview

**Solutions**:

- Check your printer's color settings
- Verify monitor calibration
- Test with different paper types
- Use standard colors for consistency
- Compare with color references

**Color Troubleshooting**:

- Print color test page
- Check printer driver settings
- Verify paper type selection
- Consider color management profiles

#### File Won't Open

**Problem**: Project file fails to load

**Solutions**:

- Verify file is a valid `.jlp` file
- Check file permissions
- Try opening in a text editor to verify JSON format
- Create a new project and recreate the design
- Check file size and corruption

**File Validation**:

```bash
# Check file format
file project.jlp

# Validate JSON
python -m json.tool project.jlp
```

### Performance Issues

#### Slow Preview Updates

**Problem**: Preview takes time to update

**Solutions**:

- Reduce the number of segments
- Use shorter text strings
- Close other applications to free memory
- Restart the application
- Check system resources

**Performance Tips**:

- Keep segment count reasonable (<50)
- Avoid very long text strings
- Close unused applications
- Ensure adequate RAM

#### Large File Sizes

**Problem**: Project files are unexpectedly large

**Solutions**:

- Check for very long text strings
- Verify reasonable number of segments
- Save and reload the project
- Contact support if issue persists

**File Size Guidelines**:

- Normal projects: <10KB
- Large projects: <100KB
- Excessive size: >1MB (investigate)

### Advanced Troubleshooting

#### Command Line Debugging

Run the application from command line to see detailed error messages:

```bash
# Run with debug output
uv run -m jackfield_labeler

# Check for Python errors
python -c "import jackfield_labeler; print('Import OK')"

# Verify PyQt6
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"
```

#### Log Files

Check for log files in your system's temporary directory:

- **Windows**: `%TEMP%\jackfield_labeler\`
- **macOS**: `/tmp/jackfield_labeler/`
- **Linux**: `/tmp/jackfield_labeler/`

#### Reset Settings

If settings become corrupted:

1. Close the application
2. Delete settings files (location varies by OS)
3. Restart the application
4. Reconfigure your preferences

#### Reinstallation

If problems persist:

1. Uninstall the application
2. Remove any remaining files
3. Reinstall using the latest version
4. Test with a simple project first

### Getting Help

#### Documentation

- Read this user guide thoroughly
- Check the README.md for installation help
- Review the architecture documentation for technical details
- Consult the API reference for development

#### Community Support

- Check GitHub issues for known problems
- Search for similar issues before reporting new ones
- Provide detailed information when reporting bugs
- Include sample project files when relevant

#### Reporting Issues

When reporting problems, include:

- Operating system and version
- Python version
- Application version
- Steps to reproduce the issue
- Error messages (if any)
- Sample project file (if relevant)
- Screenshots of the problem

**Issue Template**:

```
**Environment:**
- OS: [Windows 10/macOS 12/Ubuntu 20.04]
- Python: [3.12.0]
- Application: [0.0.1]

**Problem:**
[Describe the issue]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. [Third step]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Additional Information:**
[Any other relevant details]
```

This comprehensive user guide should help you make the most of the Jackfield Labeler application. For additional support or feature requests, please visit the project's GitHub repository.
