"""
Strip rendering utilities for preview and PNG export.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QWidget

from jackfield_labeler.models.label_strip import LabelStrip
from jackfield_labeler.models.text_format import TextFormat


class StripRenderer:
    """Renders label strips to various formats."""

    def __init__(self, label_strip: LabelStrip, scale_factor: float = 10.0):
        """
        Initialize the strip renderer.

        Args:
            label_strip: The label strip to render
            scale_factor: Pixels per mm for rendering (default 10 = 10px per mm)
        """
        self.label_strip = label_strip
        self.scale_factor = scale_factor

    def render_to_pixmap(self) -> QPixmap:
        """
        Render the strip to a QPixmap.

        Returns:
            QPixmap containing the rendered strip
        """
        if not self.label_strip or self.label_strip.get_total_width() == 0:
            # Return empty pixmap for empty strips
            return QPixmap(100, 50)

        # Calculate dimensions in pixels
        strip_width_mm = self.label_strip.get_total_width()
        strip_height_mm = self.label_strip.height
        width_px = int(strip_width_mm * self.scale_factor)
        height_px = int(strip_height_mm * self.scale_factor)

        # Create pixmap
        pixmap = QPixmap(width_px, height_px)
        pixmap.fill(Qt.GlobalColor.white)

        # Create painter
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the strip
        self._draw_strip(painter, 0, 0, width_px, height_px)

        painter.end()
        return pixmap

    def render_to_widget(self, widget: QWidget) -> None:
        """
        Render the strip directly to a widget's paint event.

        Args:
            widget: The widget to render to
        """
        if not hasattr(widget, "paintEvent"):
            return

        # This method should be called from within a widget's paintEvent
        # The actual painting will be done by the widget using _draw_strip

    def save_to_png(self, output_path: str, dpi: int = 300) -> bool:
        """
        Save the strip as a PNG file.

        Args:
            output_path: Path where the PNG should be saved
            dpi: DPI for the output image (default 300)

        Returns:
            True if PNG was saved successfully, False otherwise
        """
        try:
            if not self.label_strip or self.label_strip.get_total_width() == 0:
                return False

            # Calculate scale factor for desired DPI
            # 1 inch = 25.4 mm, so pixels per mm = dpi / 25.4
            png_scale_factor = dpi / 25.4

            # Calculate dimensions in pixels
            strip_width_mm = self.label_strip.get_total_width()
            strip_height_mm = self.label_strip.height
            width_px = int(strip_width_mm * png_scale_factor)
            height_px = int(strip_height_mm * png_scale_factor)

            # Create high-resolution pixmap
            pixmap = QPixmap(width_px, height_px)
            pixmap.fill(Qt.GlobalColor.white)

            # Create painter
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

            # Draw the strip at high resolution
            self._draw_strip_scaled(painter, 0, 0, width_px, height_px, png_scale_factor)

            painter.end()

            # Save to PNG
            return pixmap.save(output_path, "PNG")

        except Exception as e:
            print(f"Error saving PNG: {e}")
            return False

    def _draw_strip(self, painter: QPainter, x: int, y: int, width: int, height: int) -> None:
        """
        Draw the strip using the default scale factor.

        Args:
            painter: QPainter to draw with
            x: X position in pixels
            y: Y position in pixels
            width: Total width in pixels
            height: Total height in pixels
        """
        self._draw_strip_scaled(painter, x, y, width, height, self.scale_factor)

    def _draw_strip_scaled(self, painter: QPainter, x: int, y: int, width: int, height: int, scale: float) -> None:
        """
        Draw the strip with a specific scale factor.

        Args:
            painter: QPainter to draw with
            x: X position in pixels
            y: Y position in pixels
            width: Total width in pixels
            height: Total height in pixels
            scale: Scale factor (pixels per mm)
        """
        current_x = x

        # Draw start segment if present (but we removed start segments, so this should be empty)
        if self.label_strip.start_segment and self.label_strip.start_segment.width > 0:
            segment_width_px = int(self.label_strip.start_segment.width * scale)
            self._draw_segment(painter, current_x, y, segment_width_px, height, self.label_strip.start_segment, scale)
            current_x += segment_width_px

        # Draw content segments
        for segment in self.label_strip.content_segments:
            segment_width_px = int(segment.width * scale)
            self._draw_segment(painter, current_x, y, segment_width_px, height, segment, scale)
            current_x += segment_width_px

        # Draw end segment if present
        if self.label_strip.end_segment and self.label_strip.end_segment.width > 0:
            segment_width_px = int(self.label_strip.end_segment.width * scale)
            self._draw_segment(painter, current_x, y, segment_width_px, height, self.label_strip.end_segment, scale)

    def _draw_segment(self, painter: QPainter, x: int, y: int, width: int, height: int, segment, scale: float) -> None:
        """
        Draw a single segment.

        Args:
            painter: QPainter to draw with
            x: X position in pixels
            y: Y position in pixels
            width: Segment width in pixels
            height: Segment height in pixels
            segment: The segment to draw
            scale: Scale factor for font sizing
        """
        # Convert colors to Qt format
        bg_color = QColor(segment.background_color.r, segment.background_color.g, segment.background_color.b)
        text_color = QColor(segment.text_color.r, segment.text_color.g, segment.text_color.b)

        # Draw background
        painter.fillRect(x, y, width, height, bg_color)

        # Draw border
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.drawRect(x, y, width, height)

        # Draw text if present
        if segment.text:
            painter.setPen(text_color)

            # Set font based on text format and scale
            font = QFont("Arial", int(self.label_strip.settings.default_font_size * scale / 10))

            # Apply text formatting
            if hasattr(segment, "text_format") and segment.text_format:
                if segment.text_format == TextFormat.BOLD:
                    font.setBold(True)
                elif segment.text_format == TextFormat.ITALIC:
                    font.setItalic(True)

            painter.setFont(font)

            # Draw text centered horizontally and vertically in the segment
            text_rect = painter.fontMetrics().boundingRect(segment.text)
            text_x = x + (width - text_rect.width()) // 2

            # Center the text vertically in the cell
            text_y = y + height // 2 + text_rect.height() // 2

            painter.drawText(text_x, text_y, segment.text)

    def get_strip_dimensions_px(self) -> tuple[int, int]:
        """
        Get the strip dimensions in pixels using the current scale factor.

        Returns:
            Tuple of (width_px, height_px)
        """
        if not self.label_strip:
            return (0, 0)

        width_mm = self.label_strip.get_total_width()
        height_mm = self.label_strip.height
        width_px = int(width_mm * self.scale_factor)
        height_px = int(height_mm * self.scale_factor)
        return (width_px, height_px)

    def get_strip_dimensions_mm(self) -> tuple[float, float]:
        """
        Get the strip dimensions in millimeters.

        Returns:
            Tuple of (width_mm, height_mm)
        """
        if not self.label_strip:
            return (0.0, 0.0)

        width_mm = self.label_strip.get_total_width()
        height_mm = self.label_strip.height
        return (width_mm, height_mm)
