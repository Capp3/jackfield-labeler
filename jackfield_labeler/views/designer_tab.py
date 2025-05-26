"""
Designer tab for creating and editing label strips.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from jackfield_labeler.models import (
    Color,
    LabelStrip,
    StandardColor,
    TextFormat,
)


class StripControlPanel(QGroupBox):
    """Panel for controlling global strip properties."""

    strip_changed = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize the strip control panel."""
        super().__init__("Strip Controls", parent)
        self.setLayout(QVBoxLayout())

        # Content cells control
        cells_layout = QHBoxLayout()
        cells_layout.addWidget(QLabel("Number of Content Cells:"))
        self.content_cells_spinbox = QSpinBox()
        self.content_cells_spinbox.setRange(0, 100)
        self.content_cells_spinbox.setValue(0)
        self.content_cells_spinbox.valueChanged.connect(self._emit_changed)
        cells_layout.addWidget(self.content_cells_spinbox)
        self.layout().addLayout(cells_layout)

        # Cell width control
        cell_width_layout = QHBoxLayout()
        cell_width_layout.addWidget(QLabel("Content Cell Width (mm):"))
        self.cell_width_spinbox = QDoubleSpinBox()
        self.cell_width_spinbox.setRange(0.001, 100.0)
        self.cell_width_spinbox.setDecimals(3)
        self.cell_width_spinbox.setValue(10.0)
        self.cell_width_spinbox.valueChanged.connect(self._emit_changed)
        cell_width_layout.addWidget(self.cell_width_spinbox)
        self.layout().addLayout(cell_width_layout)

        # Start label width control
        start_width_layout = QHBoxLayout()
        start_width_layout.addWidget(QLabel("Start Label Width (mm):"))
        self.start_width_spinbox = QDoubleSpinBox()
        self.start_width_spinbox.setRange(0.0, 100.0)
        self.start_width_spinbox.setDecimals(3)
        self.start_width_spinbox.setValue(0.0)
        self.start_width_spinbox.valueChanged.connect(self._emit_changed)
        start_width_layout.addWidget(self.start_width_spinbox)
        self.layout().addLayout(start_width_layout)

        # End label width control
        end_width_layout = QHBoxLayout()
        end_width_layout.addWidget(QLabel("End Label Width (mm):"))
        self.end_width_spinbox = QDoubleSpinBox()
        self.end_width_spinbox.setRange(0.0, 100.0)
        self.end_width_spinbox.setDecimals(3)
        self.end_width_spinbox.setValue(0.0)
        self.end_width_spinbox.valueChanged.connect(self._emit_changed)
        end_width_layout.addWidget(self.end_width_spinbox)
        self.layout().addLayout(end_width_layout)

        # Strip height control
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Strip Height (mm):"))
        self.height_spinbox = QDoubleSpinBox()
        self.height_spinbox.setRange(LabelStrip.MIN_HEIGHT, LabelStrip.MAX_HEIGHT)
        self.height_spinbox.setDecimals(1)
        self.height_spinbox.setValue(5.0)
        self.height_spinbox.valueChanged.connect(self._emit_changed)
        height_layout.addWidget(self.height_spinbox)
        self.layout().addLayout(height_layout)

        # Total width display
        total_width_layout = QHBoxLayout()
        total_width_layout.addWidget(QLabel("Total Strip Width (mm):"))
        self.total_width_label = QLabel("0.0")
        total_width_layout.addWidget(self.total_width_label)
        self.layout().addLayout(total_width_layout)

    def _emit_changed(self):
        """Emit the strip_changed signal."""
        self.strip_changed.emit()

    def get_values(self):
        """Get the control values as a dictionary."""
        return {
            "content_cells": self.content_cells_spinbox.value(),
            "cell_width": self.cell_width_spinbox.value(),
            "start_width": self.start_width_spinbox.value(),
            "end_width": self.end_width_spinbox.value(),
            "height": self.height_spinbox.value(),
        }

    def set_values(self, values):
        """Set the control values from a dictionary."""
        self.content_cells_spinbox.setValue(values.get("content_cells", 0))
        self.cell_width_spinbox.setValue(values.get("cell_width", 10.0))
        self.start_width_spinbox.setValue(values.get("start_width", 0.0))
        self.end_width_spinbox.setValue(values.get("end_width", 0.0))
        self.height_spinbox.setValue(values.get("height", 5.0))

    def update_total_width(self, width):
        """Update the total width display."""
        self.total_width_label.setText(f"{width:.1f}")


class SegmentTable(QTableWidget):
    """Table for editing segment properties."""

    segment_changed = pyqtSignal()

    # Column indices
    ID_COL = 0
    TEXT_COL = 1
    FORMAT_COL = 2
    TEXT_COLOR_COL = 3
    BG_COLOR_COL = 4

    def __init__(self, parent=None):
        """Initialize the segment table."""
        super().__init__(0, 5, parent)

        # Set headers
        self.setHorizontalHeaderLabels(["ID", "Text", "Format", "Text Color", "Background Color"])

        # Set column properties
        header = self.horizontalHeader()
        header.setSectionResizeMode(self.ID_COL, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.TEXT_COL, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(self.FORMAT_COL, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.TEXT_COLOR_COL, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.BG_COLOR_COL, QHeaderView.ResizeMode.ResizeToContents)

        # Connect signals
        self.cellChanged.connect(self._on_cell_changed)

    def _on_cell_changed(self, row, col):
        """Handle cell content changes."""
        if col == self.TEXT_COL:
            self.segment_changed.emit()

    def clear_segments(self):
        """Clear all segments from the table."""
        self.setRowCount(0)

    def add_segment(self, segment_id, text=""):
        """Add a new segment to the table."""
        row = self.rowCount()
        self.insertRow(row)

        # Set ID (non-editable)
        id_item = QTableWidgetItem(segment_id)
        id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row, self.ID_COL, id_item)

        # Set text
        text_item = QTableWidgetItem(text)
        self.setItem(row, self.TEXT_COL, text_item)

        # Create format combobox
        format_combo = QComboBox()
        for fmt in TextFormat:
            format_combo.addItem(str(fmt), fmt)
        format_combo.currentIndexChanged.connect(lambda: self.segment_changed.emit())
        self.setCellWidget(row, self.FORMAT_COL, format_combo)

        # Create text color combobox
        text_color_combo = QComboBox()
        for color in StandardColor:
            text_color_combo.addItem(color.name.title(), color)
        text_color_combo.currentIndexChanged.connect(lambda: self.segment_changed.emit())
        self.setCellWidget(row, self.TEXT_COLOR_COL, text_color_combo)

        # Create background color combobox
        bg_color_combo = QComboBox()
        for color in StandardColor:
            bg_color_combo.addItem(color.name.title(), color)
        bg_color_combo.currentIndexChanged.connect(lambda: self.segment_changed.emit())
        self.setCellWidget(row, self.BG_COLOR_COL, bg_color_combo)

        # Set default background color to white
        bg_color_combo.setCurrentText("White")

    def get_segment_data(self, row):
        """Get the data for a segment row."""
        # Get widgets and values
        text = self.item(row, self.TEXT_COL).text()

        format_combo = self.cellWidget(row, self.FORMAT_COL)
        text_format = format_combo.currentData()

        text_color_combo = self.cellWidget(row, self.TEXT_COLOR_COL)
        text_color = text_color_combo.currentData()

        bg_color_combo = self.cellWidget(row, self.BG_COLOR_COL)
        bg_color = bg_color_combo.currentData()

        return {
            "text": text,
            "text_format": text_format,
            "text_color": text_color,
            "bg_color": bg_color,
        }

    def set_segment_data(self, row, data):
        """Set the data for a segment row."""
        # Set text
        text_item = QTableWidgetItem(data.get("text", ""))
        self.setItem(row, self.TEXT_COL, text_item)

        # Set format
        format_combo = self.cellWidget(row, self.FORMAT_COL)
        text_format = data.get("text_format", TextFormat.NORMAL)
        for i in range(format_combo.count()):
            if format_combo.itemData(i) == text_format:
                format_combo.setCurrentIndex(i)
                break

        # Set text color
        text_color_combo = self.cellWidget(row, self.TEXT_COLOR_COL)
        text_color = data.get("text_color", StandardColor.BLACK)
        for i in range(text_color_combo.count()):
            if text_color_combo.itemData(i) == text_color:
                text_color_combo.setCurrentIndex(i)
                break

        # Set background color
        bg_color_combo = self.cellWidget(row, self.BG_COLOR_COL)
        bg_color = data.get("bg_color", StandardColor.WHITE)
        for i in range(bg_color_combo.count()):
            if bg_color_combo.itemData(i) == bg_color:
                bg_color_combo.setCurrentIndex(i)
                break


class StripPreview(QFrame):
    """Preview panel for the label strip."""

    def __init__(self, parent=None):
        """Initialize the preview panel."""
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(100)

        # Add a "Preview not yet implemented" label
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Preview not yet implemented", alignment=Qt.AlignmentFlag.AlignCenter))


class DesignerTab(QWidget):
    """Tab for designing label strips."""

    def __init__(self, parent=None):
        """Initialize the designer tab."""
        super().__init__(parent)

        self.strip = LabelStrip()

        # Create main layout
        main_layout = QVBoxLayout(self)

        # Create strip control panel
        self.control_panel = StripControlPanel()
        self.control_panel.strip_changed.connect(self.update_strip_from_controls)
        main_layout.addWidget(self.control_panel)

        # Create segment table
        table_group = QGroupBox("Label Segments")
        table_layout = QVBoxLayout(table_group)

        self.segment_table = SegmentTable()
        self.segment_table.segment_changed.connect(self.update_strip_from_table)

        # Wrap the table in a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.segment_table)
        scroll_area.setWidgetResizable(True)
        table_layout.addWidget(scroll_area)

        main_layout.addWidget(table_group)

        # Create preview panel
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)
        self.preview = StripPreview()
        preview_layout.addWidget(self.preview)
        main_layout.addWidget(preview_group)

        # Create action buttons
        button_layout = QHBoxLayout()

        self.generate_pdf_button = QPushButton("Generate PDF")
        self.generate_pdf_button.clicked.connect(self.generate_pdf)
        button_layout.addWidget(self.generate_pdf_button)

        self.save_button = QPushButton("Save Project")
        self.save_button.clicked.connect(self.save_project)
        button_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Project")
        self.load_button.clicked.connect(self.load_project)
        button_layout.addWidget(self.load_button)

        main_layout.addLayout(button_layout)

        # Initialize UI state
        self.reset_ui()

    def reset_ui(self):
        """Reset the UI to match the current strip model."""
        # Create a new empty strip
        self.strip = LabelStrip()

        # Set control panel values
        self.control_panel.set_values({
            "content_cells": 0,
            "cell_width": self.strip.content_cell_width,
            "start_width": 0.0,
            "end_width": 0.0,
            "height": self.strip.height,
        })

        # Clear the segment table
        self.segment_table.clear_segments()

        # Update total width display
        self.control_panel.update_total_width(self.strip.get_total_width())

    def update_strip_from_controls(self):
        """Update the strip model from control panel values."""
        values = self.control_panel.get_values()

        # Update strip properties
        self.strip.height = values["height"]
        self.strip.content_cell_width = values["cell_width"]

        # Update start segment
        if values["start_width"] > 0:
            self.strip.set_start_segment(width=values["start_width"])
        else:
            self.strip.set_start_segment(width=0)

        # Update end segment
        if values["end_width"] > 0:
            self.strip.set_end_segment(width=values["end_width"])
        else:
            self.strip.set_end_segment(width=0)

        # Update content segments
        self.strip.set_content_segment_count(values["content_cells"])

        # Update UI
        self.update_table_from_strip()
        self.control_panel.update_total_width(self.strip.get_total_width())

    def update_strip_from_table(self):
        """Update the strip model from segment table values."""
        # Start segment
        if self.strip.start_segment is not None:
            row = 0
            data = self.segment_table.get_segment_data(row)
            self.strip.start_segment.text = data["text"]
            self.strip.start_segment.text_format = data["text_format"]
            self.strip.start_segment.text_color = Color.from_standard(data["text_color"])
            self.strip.start_segment.background_color = Color.from_standard(data["bg_color"])

            start_row_offset = 1
        else:
            start_row_offset = 0

        # Content segments
        for i, segment in enumerate(self.strip.content_segments):
            row = start_row_offset + i
            data = self.segment_table.get_segment_data(row)
            segment.text = data["text"]
            segment.text_format = data["text_format"]
            segment.text_color = Color.from_standard(data["text_color"])
            segment.background_color = Color.from_standard(data["bg_color"])

        # End segment
        if self.strip.end_segment is not None:
            row = start_row_offset + len(self.strip.content_segments)
            data = self.segment_table.get_segment_data(row)
            self.strip.end_segment.text = data["text"]
            self.strip.end_segment.text_format = data["text_format"]
            self.strip.end_segment.text_color = Color.from_standard(data["text_color"])
            self.strip.end_segment.background_color = Color.from_standard(data["bg_color"])

    def update_table_from_strip(self):
        """Update the segment table to match the strip model."""
        # Clear the table first
        self.segment_table.clear_segments()

        # Add segments to table
        if self.strip.start_segment is not None:
            self.segment_table.add_segment("L Start", self.strip.start_segment.text)

        for segment in self.strip.content_segments:
            self.segment_table.add_segment(segment.id, segment.text)

        if self.strip.end_segment is not None:
            self.segment_table.add_segment("L End", self.strip.end_segment.text)

    def save_project(self):
        """Save the current project."""
        # To be implemented
        pass

    def load_project(self):
        """Load a project from file."""
        # To be implemented
        pass

    def generate_pdf(self):
        """Generate a PDF of the current label strip."""
        # To be implemented
        pass
