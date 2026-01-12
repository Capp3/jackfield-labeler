"""
Preview tab for viewing label strips.
"""

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QResizeEvent
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from jackfield_labeler.models import LabelStrip
from jackfield_labeler.utils.pdf_generator import PDFGenerator
from jackfield_labeler.utils.strip_renderer import StripRenderer

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QWidget as QWidgetType
else:
    QWidgetType = QWidget  # Runtime alias for type annotations


class StripPreviewWidget(QGraphicsView):
    """Widget that displays a visual preview of the label strip on a page."""

    scene: QGraphicsScene  # type: ignore[assignment]  # Override method with attribute

    def __init__(self, parent: QWidgetType | None = None) -> None:
        """Initialize the preview widget."""
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setMinimumSize(500, 400)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.strip: LabelStrip | None = None
        self.pixmap_item: QGraphicsPixmapItem | None = None

    def update_preview(self, strip: LabelStrip) -> None:
        """Update the preview with a new label strip."""
        self.strip = strip
        self.scene.clear()

        if not strip or strip.get_total_width() == 0:
            self.pixmap_item = None
            return

        # Get paper dimensions in points
        paper_size_pts = PDFGenerator.PAPER_SIZES.get(strip.settings.paper_size)
        if paper_size_pts is None:
            return
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

    def resizeEvent(self, event: QResizeEvent) -> None:  # pylint: disable=invalid-name
        """Handle resize events to update the preview scale."""
        # Qt override method - must match Qt naming convention
        super().resizeEvent(event)
        if self.strip:
            self.update_preview(self.strip)


class StripInfoPanel(QFrame):
    """Panel showing information about the strip."""

    def __init__(self, parent: QWidgetType | None = None) -> None:
        """Initialize the info panel."""
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.setMaximumHeight(140)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(16, 16, 16, 16)

        # Title
        title_label = QLabel("📊 Strip Information")
        layout.addWidget(title_label)

        # Info labels
        self.dimensions_label = QLabel("Dimensions: -")
        self.segments_label = QLabel("Segments: -")
        self.end_text_label = QLabel("End Text: -")

        layout.addWidget(self.dimensions_label)
        layout.addWidget(self.segments_label)
        layout.addWidget(self.end_text_label)

        layout.addStretch()

    def update_info(self, strip: LabelStrip) -> None:
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

    def __init__(self, parent: QWidgetType | None = None) -> None:
        """Initialize the preview tab."""
        super().__init__(parent)

        # Create main layout with improved spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # Create info panel
        self.info_panel = StripInfoPanel()
        main_layout.addWidget(self.info_panel)

        # Create preview area
        self.preview_widget = StripPreviewWidget()
        main_layout.addWidget(self.preview_widget, 1)

        # Create export buttons with improved styling
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        self.export_png_button = QPushButton("🖼️ Export PNG")
        self.export_png_button.clicked.connect(self.export_png)  # type: ignore[attr-defined]
        button_layout.addWidget(self.export_png_button)

        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        # Initialize state
        self.current_strip: LabelStrip | None = None

    def update_preview(self, strip: LabelStrip) -> None:
        """Update the preview with a new label strip."""
        self.current_strip = strip
        self.preview_widget.update_preview(strip)
        self.info_panel.update_info(strip)

        # Enable/disable export button
        has_content = strip is not None and strip.get_total_width() > 0
        self.export_png_button.setEnabled(has_content)

    def export_png(self) -> None:
        """Export the current strip as a PNG file."""
        if self.current_strip is None or self.current_strip.get_total_width() == 0:
            return

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

        except Exception as e:  # pylint: disable=broad-exception-caught
            # GUI error handler - catch all exceptions to show user-friendly error
            QMessageBox.critical(self, "PNG Export Error", f"An unexpected error occurred:\n{e!s}")
