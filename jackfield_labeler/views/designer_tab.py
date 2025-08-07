"""
Designer tab for creating and editing label strips.
"""

import os
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
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
        super().__init__("🎛️ Strip Controls", parent)
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(12)
        self.layout().setContentsMargins(16, 20, 16, 16)

        # Content cells control
        cells_layout = QHBoxLayout()
        cells_layout.setSpacing(8)
        cells_label = QLabel("Number of Content Cells:")
        cells_label.setMinimumWidth(180)
        cells_layout.addWidget(cells_label)
        self.content_cells_spinbox = QSpinBox()
        self.content_cells_spinbox.setRange(0, 100)
        self.content_cells_spinbox.setValue(0)
        self.content_cells_spinbox.setMinimumWidth(100)
        self.content_cells_spinbox.valueChanged.connect(self._emit_changed)
        cells_layout.addWidget(self.content_cells_spinbox)
        cells_layout.addStretch()
        self.layout().addLayout(cells_layout)

        # Cell width control
        cell_width_layout = QHBoxLayout()
        cell_width_layout.setSpacing(8)
        cell_width_label = QLabel("Content Cell Width (mm):")
        cell_width_label.setMinimumWidth(180)
        cell_width_layout.addWidget(cell_width_label)
        self.cell_width_spinbox = QDoubleSpinBox()
        self.cell_width_spinbox.setRange(0.001, 100.0)
        self.cell_width_spinbox.setDecimals(3)
        self.cell_width_spinbox.setValue(10.0)
        self.cell_width_spinbox.setMinimumWidth(100)
        self.cell_width_spinbox.valueChanged.connect(self._emit_changed)
        cell_width_layout.addWidget(self.cell_width_spinbox)
        cell_width_layout.addStretch()
        self.layout().addLayout(cell_width_layout)

        # End label width control
        end_width_layout = QHBoxLayout()
        end_width_layout.setSpacing(8)
        end_width_label = QLabel("End Label Width (both ends, mm):")
        end_width_label.setMinimumWidth(180)
        end_width_layout.addWidget(end_width_label)
        self.end_width_spinbox = QDoubleSpinBox()
        self.end_width_spinbox.setRange(0.0, 100.0)
        self.end_width_spinbox.setDecimals(3)
        self.end_width_spinbox.setValue(0.0)
        self.end_width_spinbox.setMinimumWidth(100)
        self.end_width_spinbox.valueChanged.connect(self._emit_changed)
        end_width_layout.addWidget(self.end_width_spinbox)
        end_width_layout.addStretch()
        self.layout().addLayout(end_width_layout)

        # End label text control
        end_text_layout = QHBoxLayout()
        end_text_layout.setSpacing(8)
        end_text_label = QLabel("End Label Text (both ends):")
        end_text_label.setMinimumWidth(180)
        end_text_layout.addWidget(end_text_label)
        self.end_text_input = QLineEdit()
        self.end_text_input.setPlaceholderText("Enter text for both end labels")
        self.end_text_input.textChanged.connect(self._emit_changed)
        end_text_layout.addWidget(self.end_text_input)
        self.layout().addLayout(end_text_layout)

        # Strip height control
        height_layout = QHBoxLayout()
        height_layout.setSpacing(8)
        height_label = QLabel("Strip Height (mm):")
        height_label.setMinimumWidth(180)
        height_layout.addWidget(height_label)
        self.height_spinbox = QDoubleSpinBox()
        self.height_spinbox.setRange(LabelStrip.MIN_HEIGHT, LabelStrip.MAX_HEIGHT)
        self.height_spinbox.setDecimals(1)
        self.height_spinbox.setValue(5.0)
        self.height_spinbox.setMinimumWidth(100)
        self.height_spinbox.valueChanged.connect(self._emit_changed)
        height_layout.addWidget(self.height_spinbox)
        height_layout.addStretch()
        self.layout().addLayout(height_layout)

        # Total width display
        total_width_layout = QHBoxLayout()
        total_width_layout.setSpacing(8)
        total_width_label = QLabel("Total Strip Width (mm):")
        total_width_label.setMinimumWidth(180)
        total_width_label.setStyleSheet("font-weight: 600; color: #e6e6e6;")
        total_width_layout.addWidget(total_width_label)
        self.total_width_label = QLabel("0.0")
        self.total_width_label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #ffffff;
                background-color: #ff6b35;
                border: 1px solid #e55a2b;
                border-radius: 4px;
                padding: 4px 8px;
                min-width: 60px;
            }
        """)
        total_width_layout.addWidget(self.total_width_label)
        total_width_layout.addStretch()
        self.layout().addLayout(total_width_layout)

    def _emit_changed(self):
        """Emit the strip_changed signal."""
        self.strip_changed.emit()

    def get_values(self):
        """Get the control values as a dictionary."""
        return {
            "content_cells": self.content_cells_spinbox.value(),
            "cell_width": self.cell_width_spinbox.value(),
            "end_width": self.end_width_spinbox.value(),
            "end_text": self.end_text_input.text(),
            "height": self.height_spinbox.value(),
        }

    def set_values(self, values):
        """Set the control values from a dictionary."""
        self.content_cells_spinbox.setValue(values.get("content_cells", 0))
        self.cell_width_spinbox.setValue(values.get("cell_width", 10.0))
        self.end_width_spinbox.setValue(values.get("end_width", 0.0))
        self.end_text_input.setText(values.get("end_text", ""))
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
    WIDTH_COL = 5

    def __init__(self, parent=None):
        """Initialize the segment table."""
        super().__init__(parent)

        # Set up table properties
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["ID", "Text", "Format", "Text Color", "Background", "Width (mm)"])

        # Configure table appearance
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(True)

        # Set column widths
        header = self.horizontalHeader()
        header.setSectionResizeMode(self.ID_COL, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(self.TEXT_COL, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(self.FORMAT_COL, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(self.TEXT_COLOR_COL, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(self.BG_COLOR_COL, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(self.WIDTH_COL, QHeaderView.ResizeMode.Fixed)

        self.setColumnWidth(self.ID_COL, 60)
        self.setColumnWidth(self.FORMAT_COL, 80)
        self.setColumnWidth(self.TEXT_COLOR_COL, 100)
        self.setColumnWidth(self.BG_COLOR_COL, 100)
        self.setColumnWidth(self.WIDTH_COL, 100)

        # Connect signals
        self.itemChanged.connect(self._on_cell_changed)

        # Apply custom styling
        self.setStyleSheet("""
            QTableWidget {
                gridline-color: #404040;
                background-color: #2b2b2b;
                alternate-background-color: #3c3c3c;
                selection-background-color: #ff6b35;
                selection-color: #ffffff;
                border: 1px solid #404040;
                border-radius: 4px;
                color: #e6e6e6;
            }

            QTableWidget::item {
                padding: 8px 12px;
                border: none;
                color: #e6e6e6;
            }

            QTableWidget::item:selected {
                background-color: #ff6b35;
                color: #ffffff;
            }

            QHeaderView::section {
                background-color: #3c3c3c;
                border: none;
                border-bottom: 2px solid #404040;
                padding: 12px 8px;
                font-weight: 600;
                color: #ff6b35;
                font-size: 11px;
            }

            QHeaderView::section:hover {
                background-color: #404040;
            }
        """)

        # Set row height to accommodate larger dropdowns
        self.verticalHeader().setDefaultSectionSize(40)

        # Additional styling for table cell widgets
        self.setStyleSheet(
            self.styleSheet()
            + """
            QTableWidget QComboBox {
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 4px 8px;
                background-color: #3c3c3c;
                color: #e6e6e6;
                min-height: 20px;
            }

            QTableWidget QComboBox:focus {
                border-color: #ff6b35;
            }

            QTableWidget QComboBox::drop-down {
                border: none;
                width: 16px;
            }

            QTableWidget QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #e6e6e6;
                margin-right: 4px;
            }

            QTableWidget QDoubleSpinBox {
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 4px 8px;
                background-color: #3c3c3c;
                color: #e6e6e6;
                min-height: 20px;
            }

            QTableWidget QDoubleSpinBox:focus {
                border-color: #ff6b35;
            }
        """
        )

    def _on_cell_changed(self, item):
        """Handle cell content changes."""
        if item.column() == self.TEXT_COL:
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

        # Create width spinbox
        width_spinbox = QDoubleSpinBox()
        width_spinbox.setRange(0.001, 100.0)
        width_spinbox.setDecimals(3)
        width_spinbox.setValue(10.0)
        width_spinbox.valueChanged.connect(lambda: self.segment_changed.emit())
        self.setCellWidget(row, self.WIDTH_COL, width_spinbox)

        # Set default colors based on settings
        # Default text color to black
        text_color_combo.setCurrentText("Black")
        # Set default background color to white
        bg_color_combo.setCurrentText("White")

    def get_segment_data(self, row):
        """Get the data for a segment row."""
        # Get widgets and values
        text_item = self.item(row, self.TEXT_COL)
        if text_item is None:
            return None
        text = text_item.text()

        format_combo = self.cellWidget(row, self.FORMAT_COL)
        if format_combo is None:
            return None
        text_format = format_combo.currentData()

        text_color_combo = self.cellWidget(row, self.TEXT_COLOR_COL)
        if text_color_combo is None:
            return None
        text_color = text_color_combo.currentData()

        bg_color_combo = self.cellWidget(row, self.BG_COLOR_COL)
        if bg_color_combo is None:
            return None
        bg_color = bg_color_combo.currentData()

        width_spinbox = self.cellWidget(row, self.WIDTH_COL)
        if width_spinbox is None:
            return None
        width = width_spinbox.value()

        return {
            "text": text,
            "text_format": text_format,
            "text_color": text_color,
            "bg_color": bg_color,
            "width": width,
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

        # Set width
        width_spinbox = self.cellWidget(row, self.WIDTH_COL)
        width = data.get("width", 10.0)
        width_spinbox.setValue(width)


class DesignerTab(QWidget):
    """Tab for designing label strips."""

    def __init__(self, parent=None):
        """Initialize the designer tab."""
        super().__init__(parent)
        
        # Track current project path for export filenames
        self._current_project_path = None

        # Create main layout with improved spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # Create horizontal split layout
        split_layout = QHBoxLayout()
        split_layout.setSpacing(16)

        # Left panel - Controls
        left_panel = QVBoxLayout()
        left_panel.setSpacing(16)

        # Add control panel
        self.control_panel = StripControlPanel()
        left_panel.addWidget(self.control_panel)

        # Add action buttons
        action_group = QGroupBox("🚀 Actions")
        action_group.setLayout(QVBoxLayout())
        action_group.layout().setSpacing(8)
        action_group.layout().setContentsMargins(16, 20, 16, 16)

        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        self.add_row_button = QPushButton("+ Add Row")
        self.add_row_button.clicked.connect(self._add_row)
        button_layout.addWidget(self.add_row_button)

        self.remove_row_button = QPushButton("- Remove Row")
        self.remove_row_button.clicked.connect(self._remove_row)
        button_layout.addWidget(self.remove_row_button)

        action_group.layout().addLayout(button_layout)

        # Add export buttons
        export_layout = QHBoxLayout()
        export_layout.setSpacing(8)

        self.generate_pdf_button = QPushButton("📄 Generate PDF")
        self.generate_pdf_button.clicked.connect(self.generate_pdf)
        export_layout.addWidget(self.generate_pdf_button)

        self.export_png_button = QPushButton("🖼️ Export PNG")
        self.export_png_button.clicked.connect(self.export_png)
        export_layout.addWidget(self.export_png_button)

        action_group.layout().addLayout(export_layout)
        left_panel.addWidget(action_group)

        # Add stretch to push controls to top
        left_panel.addStretch()

        # Right panel - Segment table
        right_panel = QVBoxLayout()
        right_panel.setSpacing(8)

        # Add table header
        table_header = QLabel("📋 Segment Properties")
        table_header.setStyleSheet("""
            QLabel {
                font-weight: 600;
                font-size: 14px;
                color: #495057;
                padding: 8px 0;
            }
        """)
        right_panel.addWidget(table_header)

        # Add segment table
        self.segment_table = SegmentTable()
        right_panel.addWidget(self.segment_table)

        # Add panels to split layout
        split_layout.addLayout(left_panel, 1)  # 1 part width
        split_layout.addLayout(right_panel, 2)  # 2 parts width

        # Add split layout to main layout
        main_layout.addLayout(split_layout)

        # Initialize strip
        self.strip = LabelStrip()

        # Connect signals
        self.control_panel.strip_changed.connect(self.update_strip_from_controls)
        self.segment_table.segment_changed.connect(self.update_strip_from_table)

        # Initialize UI
        self.reset_ui()

    def reset_ui(self):
        """Reset the UI to match the current strip model."""
        # Create a new empty strip
        self.strip = LabelStrip()

        # Set control panel values
        self.control_panel.set_values({
            "content_cells": 0,
            "cell_width": self.strip.content_cell_width,
            "end_width": 0.0,
            "end_text": "",
            "height": self.strip.height,
        })

        # Clear the segment table
        self.segment_table.clear_segments()

        # Update total width display
        self.control_panel.update_total_width(self.strip.get_total_width())

    def set_project_path(self, project_path: str | None):
        """Set the current project path for export filename generation."""
        self._current_project_path = project_path

    def _get_default_export_filename(self, extension: str) -> str:
        """Generate default export filename based on current project name."""
        if self._current_project_path:
            # Extract project name without extension
            project_name = os.path.splitext(os.path.basename(self._current_project_path))[0]
            return f"{project_name}.{extension}"
        else:
            # Fallback for unsaved projects
            return f"label_strip.{extension}"

    def load_label_strip(self, label_strip: LabelStrip):
        """Load a label strip into the UI."""
        self.strip = label_strip

        # Calculate control values from the loaded strip
        end_width = self.strip.end_segment.width if self.strip.end_segment else 0.0
        end_text = self.strip.end_segment.text if self.strip.end_segment else ""
        content_cells = len(self.strip.content_segments)

        # Set control panel values
        self.control_panel.set_values({
            "content_cells": content_cells,
            "cell_width": self.strip.content_cell_width,
            "end_width": end_width,
            "end_text": end_text,
            "height": self.strip.height,
        })

        # Update the table to match the loaded strip
        self.update_table_from_strip()

        # Update total width display
        self.control_panel.update_total_width(self.strip.get_total_width())

    def update_strip_from_controls(self):
        """Update the strip model from control panel values."""
        values = self.control_panel.get_values()

        # Update strip properties
        self.strip.height = values["height"]
        self.strip.content_cell_width = values["cell_width"]

        # Update end segment
        if values["end_width"] > 0:
            # Set both end and start segments with the same properties
            self.strip.set_end_segment(width=values["end_width"])
            self.strip.set_start_segment(width=values["end_width"])

            # Set the end segment text from the control panel
            if self.strip.end_segment:
                self.strip.end_segment.text = values["end_text"]

            # Set the start segment text to be the same as the end segment
            if self.strip.start_segment:
                self.strip.start_segment.text = values["end_text"]
        else:
            # If no end segment, remove both start and end segments
            self.strip.set_end_segment(width=0)
            self.strip.set_start_segment(width=0)

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
            if data is not None:
                self.strip.start_segment.text = data["text"]
                self.strip.start_segment.text_format = data["text_format"]
                self.strip.start_segment.text_color = Color.from_standard(data["text_color"])
                self.strip.start_segment.background_color = Color.from_standard(data["bg_color"])
                self.strip.start_segment.width = data["width"]

            start_row_offset = 1
        else:
            start_row_offset = 0

        # Content segments
        for i, segment in enumerate(self.strip.content_segments):
            row = start_row_offset + i
            data = self.segment_table.get_segment_data(row)
            if data is not None:
                segment.text = data["text"]
                segment.text_format = data["text_format"]
                segment.text_color = Color.from_standard(data["text_color"])
                segment.background_color = Color.from_standard(data["bg_color"])
                segment.width = data["width"]

        # End segment
        if self.strip.end_segment is not None:
            row = start_row_offset + len(self.strip.content_segments)
            data = self.segment_table.get_segment_data(row)
            if data is not None:
                self.strip.end_segment.text = data["text"]
                self.strip.end_segment.text_format = data["text_format"]
                self.strip.end_segment.text_color = Color.from_standard(data["text_color"])
                self.strip.end_segment.background_color = Color.from_standard(data["bg_color"])
                self.strip.end_segment.width = data["width"]

                # Synchronize start segment with end segment if both exist
                if self.strip.start_segment is not None:
                    self.strip.start_segment.text = self.strip.end_segment.text
                    self.strip.start_segment.text_format = self.strip.end_segment.text_format
                    self.strip.start_segment.text_color = self.strip.end_segment.text_color
                    self.strip.start_segment.background_color = self.strip.end_segment.background_color

    def update_table_from_strip(self):
        """Update the segment table to match the strip model."""
        # Temporarily disconnect the signal to prevent premature updates
        self.segment_table.segment_changed.disconnect(self.update_strip_from_table)

        try:
            # Clear the table first
            self.segment_table.clear_segments()

            # Add segments to table
            if self.strip.start_segment is not None:
                self.segment_table.add_segment("L Start", self.strip.start_segment.text)

            for segment in self.strip.content_segments:
                self.segment_table.add_segment(segment.id, segment.text)

            if self.strip.end_segment is not None:
                self.segment_table.add_segment("L End", self.strip.end_segment.text)
        finally:
            # Reconnect the signal
            self.segment_table.segment_changed.connect(self.update_strip_from_table)

    def _add_row(self):
        """Add a new content segment to the strip."""
        # Get current content cell count
        current_count = len(self.strip.content_segments)

        # Add one more content segment
        self.strip.set_content_segment_count(current_count + 1)

        # Update the control panel to reflect the new count
        values = self.control_panel.get_values()
        values["content_cells"] = current_count + 1
        self.control_panel.set_values(values)

        # Update the table to show the new segment
        self.update_table_from_strip()

        # Update total width display
        self.control_panel.update_total_width(self.strip.get_total_width())

    def _remove_row(self):
        """Remove the last content segment from the strip."""
        # Get current content cell count
        current_count = len(self.strip.content_segments)

        # Don't allow removing if there are no content segments
        if current_count <= 0:
            return

        # Remove one content segment
        self.strip.set_content_segment_count(current_count - 1)

        # Update the control panel to reflect the new count
        values = self.control_panel.get_values()
        values["content_cells"] = current_count - 1
        self.control_panel.set_values(values)

        # Update the table to show the removed segment
        self.update_table_from_strip()

        # Update total width display
        self.control_panel.update_total_width(self.strip.get_total_width())

    def save_project(self):
        """Save the current project."""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        from jackfield_labeler.utils import ProjectManager

        # Get file path to save to
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Project", "untitled.jlp", ProjectManager.PROJECT_FILTER)

        if not file_path:
            return  # User cancelled

        # Save the project
        try:
            success = ProjectManager.save_project(self.strip, file_path)

            if success:
                QMessageBox.information(self, "Project Saved", f"Project has been saved to:\n{file_path}")
            else:
                QMessageBox.critical(self, "Save Error", f"Failed to save project to:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"An unexpected error occurred while saving the project:\n{e!s}")

    def load_project(self):
        """Load a project from file."""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        from jackfield_labeler.utils import ProjectManager

        # Get file path to load from
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Project", "", ProjectManager.PROJECT_FILTER)

        if not file_path:
            return  # User cancelled

        # Load the project
        try:
            label_strip = ProjectManager.load_project(file_path)
            if label_strip is None:
                QMessageBox.critical(
                    self,
                    "Load Error",
                    f"Failed to load project from:\n{file_path}\n\nThe file may be corrupted or in an unsupported format.",
                )
                return

            # Load the label strip into the UI
            self.load_label_strip(label_strip)

            QMessageBox.information(self, "Project Loaded", f"Project has been loaded from:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"An unexpected error occurred while loading the project:\n{e!s}")

    def generate_pdf(self):
        """Generate a PDF of the current label strip."""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        from jackfield_labeler.utils import PDFGenerator

        # Check if there are any segments to generate
        if self.strip.get_total_width() == 0:
            QMessageBox.warning(
                self, "No Content", "Please add some segments to the label strip before generating a PDF."
            )
            return

        # Get output file path
        default_filename = self._get_default_export_filename("pdf")
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", default_filename, "PDF Files (*.pdf);;All Files (*)"
        )

        if not file_path:
            return  # User cancelled

        try:
            # Create PDF generator
            pdf_generator = PDFGenerator(self.strip)

            # Generate the PDF using rotation from settings
            success = pdf_generator.generate_pdf(file_path)

            if success:
                QMessageBox.information(self, "PDF Generated", f"PDF has been saved to:\n{file_path}")
            else:
                QMessageBox.critical(
                    self,
                    "PDF Generation Failed",
                    "An error occurred while generating the PDF. Please check your label strip configuration.",
                )

        except Exception as e:
            QMessageBox.critical(self, "PDF Generation Error", f"An unexpected error occurred:\n{e!s}")

    def export_png(self):
        """Export the current strip as a PNG file."""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        from jackfield_labeler.utils import StripRenderer

        # Check if there are any segments to generate
        if self.strip.get_total_width() == 0:
            QMessageBox.warning(
                self, "No Content", "Please add some segments to the label strip before exporting a PNG."
            )
            return

        # Get output file path
        default_filename = self._get_default_export_filename("png")
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export PNG", default_filename, "PNG Files (*.png);;All Files (*)"
        )

        if not file_path:
            return  # User cancelled

        try:
            # Create high-resolution renderer for PNG export
            renderer = StripRenderer(self.strip)

            # Save PNG at 300 DPI
            success = renderer.save_to_png(file_path, dpi=300)

            if success:
                QMessageBox.information(self, "PNG Exported", f"PNG has been saved to:\n{file_path}")
            else:
                QMessageBox.critical(
                    self,
                    "PNG Export Failed",
                    "An error occurred while exporting the PNG. Please check your label strip configuration.",
                )

        except Exception as e:
            QMessageBox.critical(self, "PNG Export Error", f"An unexpected error occurred:\n{e!s}")
