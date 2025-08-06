"""
Preview tab for viewing label strips.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from jackfield_labeler.models import LabelStrip
from jackfield_labeler.utils.pdf_generator import PDFGenerator
from jackfield_labeler.utils.strip_renderer import StripRenderer


class StripPreviewWidget(QGraphicsView):
    """Widget that displays a visual preview of the label strip on a page."""

    def __init__(self, parent=None):
        """Initialize the preview widget."""
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: lightgray;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.strip = None
        self.pixmap_item = None

    def update_preview(self, strip: LabelStrip):
        """Update the preview with a new label strip."""
        self.strip = strip
        self.scene.clear()

        if not strip or strip.get_total_width() == 0:
            self.pixmap_item = None
            return

        # Get paper dimensions in points
        paper_size_pts = PDFGenerator.PAPER_SIZES.get(strip.settings.paper_size)
        page_width_pts, page_height_pts = paper_size_pts

        # Determine the scale to fit the view
        view_rect = self.viewport().rect()
        scale_x = view_rect.width() / page_width_pts if page_width_pts > 0 else 1
        scale_y = view_rect.height() / page_height_pts if page_height_pts > 0 else 1
        scale = min(scale_x, scale_y) * 0.95  # 95% to leave a margin

        # Create renderer with the calculated scale
        renderer = StripRenderer(strip, scale_factor=scale)

        # Render the strip on a page
        pixmap = renderer.render_to_pixmap_on_page(int(page_width_pts * scale), int(page_height_pts * scale))

        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)
        self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        """Handle resize events to update the preview scale."""
        super().resizeEvent(event)
        if self.strip:
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

        # Create preview area
        self.preview_widget = StripPreviewWidget()
        main_layout.addWidget(self.preview_widget, 1)

        # Create export buttons
        button_layout = QHBoxLayout()

        self.export_png_button = QPushButton("Export PNG")
        self.export_png_button.clicked.connect(self.export_png)
        button_layout.addWidget(self.export_png_button)

        button_layout.addStretch()

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
