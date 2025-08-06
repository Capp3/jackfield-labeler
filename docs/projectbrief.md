# Jackfield Labeler

## 1. Introduction & Project Goals 🎯

* **Primary Goal:** To create a desktop application that allows users to design and print custom label strips for 19" equipment rack jackfields.
* **Label Dimensions:** Strips are typically 5mm to 12mm tall and can be up to 400mm to 500mm wide (though the application should support user-defined widths).
* **Key Innovation:** The application intelligently rotates long label strips to fit diagonally on standard paper sizes (e.g., A4, Letter), enabling printing on common office printers.
* **User Interface:** Provides an intuitive GUI for entering label text, defining segment properties (width, colors), and configuring output settings.
* **Output:** The final output is a **PDF document**, ready for printing.

## 2. Target User 🧑‍💻

* Audio engineers, broadcast technicians, IT professionals, lab managers, or anyone needing to create clear, custom labels for patch panels, jackfields, and other rack-mounted equipment.

## 3. Technical Details 🛠️

* **Programming Language:** Python 3.12+
* **GUI Framework:** PyQt6 (≥6.9.0)
* **PDF Generation:** ReportLab (≥4.4.1) for professional PDF output
* **Platform:** Cross-platform compatibility (Windows, macOS, Linux) leveraging Python and PyQt6
* **Package Manager:** This application uses UV and NOT pip. Dependencies should be added with `uv add` and the application should be run using `uv run -m jackfield_labeler`

## 4. Core Functionality ⚙️

### 4.1. Label Strip Design

* **Overall Strip Height:** User-definable (e.g., in millimeters, with one decimal place).
* **Strip Composition:** A single label strip is composed of several horizontal segments:
  * An optional **"Start Label"** segment (e.g., for a general title or identifier). Its width can be set to zero if not used.
  * A user-defined number of main **"Content Cells"** (for individual jack labels).
  * An optional **"End Label"** segment. Its width can be set to zero if not used.
* **Segment Widths:**
  * **Content Cell Width (mm):** A uniform width applied to all main content cells. Settable up to 3 decimal places.
  * **Start Label Width (mm):** A separately definable width for the "Start Label" segment. Settable up to 3 decimal places.
  * **End Label Width (mm):** A separately definable width for the "End Label" segment. Settable up to 3 decimal places.
* **Total Strip Width:** Automatically calculated and displayed to the user based on the number of content cells and the defined widths of all segments.

### 4.2. Label Segment Configuration (Spreadsheet-like Interface)

The main interface features a table where each row defines a segment of the *single* label strip being designed.

* **Rows:**
  * The first row represents the "Start Label" segment (labeled "L Start" or similar, dynamically present based on its defined width).
  * Subsequent rows represent the "Content Cells" (labeled "1", "2", "3", ...).
  * The last row represents the "End Label" segment (labeled "L End" or similar, dynamically present based on its defined width).
* **Columns for each segment row:**
  * **Segment ID:** Read-only (e.g., "L Start", "1", "2", ..., "L End").
  * **Text:** The text to display on that segment of the label.
  * **Text Format:** Dropdown or radio buttons (Normal, Bold, Italic, Bold & Italic).
  * **Text Color:** Color picker/dropdown (e.g., Black, White, Red initially).
  * **Background Color:** Color picker/dropdown (e.g., White, Black, Red, Orange, Yellow, Green, Blue, Purple initially).

### 4.3. PDF Output & Printing Preparation

* Generate a high-quality PDF of the designed label strip.
* **Automatic Rotation for Printing:**
  * A core capability of the application is to handle labels that are too long for the selected paper width.
  * If the total strip width exceeds the effective printable width of the selected paper size, the application calculates the necessary rotation angle to print the strip diagonally across the page.
  * The PDF is generated with the strip pre-rotated and positioned optimally on the selected paper size, considering specified margins.
* **Paper Size Selection:** User can choose from standard paper sizes (A0-A4, Letter, Legal, Tabloid).

### 4.4. Real-time Preview ✨

* A dedicated Preview tab in the UI showing a scaled visual representation of the label strip as it's being designed. This preview updates dynamically as the user changes properties or text.

## 5. Application Layout 🖼️

The application consists of three main tabs:

### 5.1. Designer Tab (Main View)

* **Global Strip Controls (Input Panel):**
  * **Number of Content Cells:** Numeric input with up/down arrows.
  * **Content Cell Width (mm):** Numeric input (e.g., `QDoubleSpinBox`), settable to 3 decimal places, with up/down arrows.
  * **End Label Width (mm):** Numeric input, 3 decimal places, up/down arrows (allows 0).
  * **End Label Text:** Text input for the end label content.
  * **Strip Height (mm):** Numeric input (e.g., 1 decimal place), up/down arrows.
  * **Total Strip Width (mm):** Read-only display, automatically updated.
* **Label Segments Table:**
  * As described in section 4.2. Rows for "Start Label", "Content Cells", and "End Label" dynamically appear/disappear or are marked as inactive if their corresponding widths are set to zero.
* **Action Buttons:**
  * `Generate PDF`
  * `Save Project`
  * `Load Project`

### 5.2. Settings Tab ⚙️

* **Paper Size:** Dropdown list (A4, A3, A2, A1, A0, Letter, Legal, Tabloid) with A3 as default.
* **Default Text Font:** Font selection dialog (e.g., `QFontDialog`) to choose from available system fonts.
* **Default Font Size (pt):** Numeric input for the font size to be used on labels.
* **Page Margins (mm):** Input fields for Top, Bottom, Left, Right margins for the PDF output. This affects the available space for printing the (potentially rotated) strip.
* **Default Text Color:** For new segments.
* **Default Background Color:** For new segments.
* **Rotation Settings:** Configurable rotation angle (0°-360°) with preset buttons for common angles.

### 5.3. Preview Tab 👁️

* **Strip Information:** Displays dimensions, segment count, and configuration details.
* **Visual Preview:** Scaled preview that updates automatically with design changes.
* **Export Options:** Direct PNG export with high resolution (300 DPI).

## 6. Non-Functional Requirements

* **Usability:** The application should be intuitive, even for users not deeply familiar with graphic design or command-line tools. Clear visual feedback is important.
* **Performance:** The UI should be responsive. PDF generation, including rotation calculations, should be reasonably fast.
* **Maintainability:** Code should be well-organized (e.g., separating UI logic, data model/strip logic, and PDF generation/rotation logic).
* **Error Handling:** Graceful handling of invalid inputs or potential issues (e.g., text overflow in a cell might be indicated in the preview).

## 7. Future Enhancements (Possible Next Steps) 🚀

* Saving and loading label design projects/templates.
* More extensive color palettes or full RGB/HSV color pickers.
* Advanced text alignment options (Horizontal: Left, Center, Right; Vertical: Top, Middle, Bottom) per segment.
* Grid lines or cut marks on the PDF output to aid cutting.
* Option to print multiple *different* label strips on a single sheet, if space allows.
* Option to print multiple copies of the *same* label strip, optimally arranged on the sheet.
* Importing label text from CSV or text files.
* Undo/Redo functionality for design changes.
* User-definable list of common strip heights or cell widths.
