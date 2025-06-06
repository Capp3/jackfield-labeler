"""
Preview tab for viewing label strips.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from jackfield_labeler.models import LabelStrip
from jackfield_labeler.utils.strip_renderer import StripRenderer


class StripPreviewWidget(QLabel):
    """Widget that displays a visual preview of the label strip."""

    def __init__(self, parent=None):
        """Initialize the preview widget."""
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(400, 100)
        self.setStyleSheet("border: 1px solid gray; background-color: white;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.strip = None
        self.renderer = None
        self.setText("No strip to preview")

    def update_preview(self, strip: LabelStrip):
        """Update the preview with a new label strip."""
        self.strip = strip

        if not strip or strip.get_total_width() == 0:
            self.setText("No strip to preview")
            self.renderer = None
            return

        # Create renderer with appropriate scale
        # Calculate scale to fit the widget nicely
        widget_width = self.width() - 20  # Leave some margin
        widget_height = self.height() - 20

        strip_width_mm = strip.get_total_width()
        strip_height_mm = strip.height

        # Calculate scale factors to fit in widget
        scale_x = widget_width / strip_width_mm if strip_width_mm > 0 else 1
        scale_y = widget_height / strip_height_mm if strip_height_mm > 0 else 1

        # Use the smaller scale to ensure it fits
        scale = min(scale_x, scale_y, 20.0)  # Cap at 20px per mm for readability
        scale = max(scale, 2.0)  # Minimum 2px per mm

        self.renderer = StripRenderer(strip, scale)

        # Render to pixmap and display
        pixmap = self.renderer.render_to_pixmap()
        self.setPixmap(pixmap)

    def resizeEvent(self, event):
        """Handle resize events to update the preview scale."""
        super().resizeEvent(event)
        if self.strip:
            # Re-render with new scale when widget is resized
            self.update_preview(self.strip)


class StripInfoPanel(QFrame):
    """Panel showing information about the strip."""

    def __init__(self, parent=None):
        """Initialize the info panel."""
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.setMaximumHeight(120)

        layout = QVBoxLayout(self)

        # Title
        title_label = QLabel("Strip Information")
        title_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(title_label)

        # Info labels
        self.dimensions_label = QLabel("Dimensions: -")
        self.segments_label = QLabel("Segments: -")
        self.end_text_label = QLabel("End Text: -")

        layout.addWidget(self.dimensions_label)
        layout.addWidget(self.segments_label)
        layout.addWidget(self.end_text_label)

        layout.addStretch()

    def update_info(self, strip: LabelStrip):
        """Update the information display."""
        if not strip or strip.get_total_width() == 0:
            self.dimensions_label.setText("Dimensions: -")
            self.segments_label.setText("Segments: -")
            self.end_text_label.setText("End Text: -")
            return

        # Calculate dimensions
        width_mm = strip.get_total_width()
        height_mm = strip.height
        self.dimensions_label.setText(f"Dimensions: {width_mm:.1f}mm x {height_mm:.1f}mm")

        # Count segments
        segment_count = len(strip.content_segments)
        if strip.end_segment and strip.end_segment.width > 0:
            segment_count += 1
        self.segments_label.setText(f"Segments: {segment_count}")

        # Show end text
        end_text = strip.end_segment.text if strip.end_segment else ""
        if end_text:
            self.end_text_label.setText(f"End Text: {end_text}")
        else:
            self.end_text_label.setText("End Text: (none)")


class PreviewTab(QWidget):
    """Tab for previewing label strips."""

    def __init__(self, parent=None):
        """Initialize the preview tab."""
        super().__init__(parent)

        # Create main layout
        main_layout = QVBoxLayout(self)

        # Create info panel
        self.info_panel = StripInfoPanel()
        main_layout.addWidget(self.info_panel)

        # Create preview area with scroll
        preview_scroll = QScrollArea()
        preview_scroll.setWidgetResizable(True)
        preview_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        preview_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.preview_widget = StripPreviewWidget()
        preview_scroll.setWidget(self.preview_widget)

        main_layout.addWidget(preview_scroll, 1)  # Give it most of the space

        # Create export buttons
        button_layout = QHBoxLayout()

        self.export_png_button = QPushButton("Export PNG")
        self.export_png_button.clicked.connect(self.export_png)
        button_layout.addWidget(self.export_png_button)

        button_layout.addStretch()  # Push buttons to the left

        main_layout.addLayout(button_layout)

        # Initialize state
        self.current_strip = None

    def update_preview(self, strip: LabelStrip):
        """Update the preview with a new label strip."""
        self.current_strip = strip
        self.preview_widget.update_preview(strip)
        self.info_panel.update_info(strip)

        # Enable/disable export button
        has_content = strip and strip.get_total_width() > 0
        self.export_png_button.setEnabled(has_content)

    def export_png(self):
        """Export the current strip as a PNG file."""
        if not self.current_strip or self.current_strip.get_total_width() == 0:
            return

        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        # Get output file path
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export PNG", "label_strip.png", "PNG Files (*.png);;All Files (*)"
        )

        if not file_path:
            return  # User cancelled

        try:
            # Create high-resolution renderer for PNG export
            renderer = StripRenderer(self.current_strip)

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
