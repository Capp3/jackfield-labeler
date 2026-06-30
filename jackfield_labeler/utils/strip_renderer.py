"""
Strip rendering utilities for preview and PNG export.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QPixmap

from jackfield_labeler.models.label_strip import LabelStrip
from jackfield_labeler.models.segment import Segment
from jackfield_labeler.models.text_format import TextFormat
from jackfield_labeler.utils.logger import get_logger

logger = get_logger(__name__)


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

    def render_to_pixmap_on_page(self, page_width_px: int, page_height_px: int) -> QPixmap:
        """
        Render the strip onto a pixmap representing the page, including rotation.

        Args:
            page_width_px: The width of the page in pixels
            page_height_px: The height of the page in pixels

        Returns:
            A QPixmap with the strip rendered on a page representation.
        """
        pixmap = QPixmap(page_width_px, page_height_px)
        pixmap.fill(QColor("lightgray"))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw a white rectangle for the paper
        painter.fillRect(0, 0, page_width_px, page_height_px, Qt.GlobalColor.white)
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.drawRect(0, 0, page_width_px - 1, page_height_px - 1)

        # Get strip dimensions in pixels
        strip_width_px, strip_height_px = self.get_strip_dimensions_px()

        # Center and rotate around the page centre
        painter.translate(page_width_px / 2, page_height_px / 2)
        painter.rotate(self.label_strip.settings.rotation_angle)
        painter.translate(-strip_width_px / 2, -strip_height_px / 2)

        # Draw the strip
        self._draw_strip(painter, 0, 0, strip_width_px, strip_height_px)

        painter.end()
        return pixmap

    def render_to_pixmap(self) -> QPixmap:
        """
        Render the strip to a QPixmap.

        Returns:
            QPixmap containing the rendered strip
        """
        if not self.label_strip or self.label_strip.get_total_width() == 0:
            return QPixmap(100, 50)

        strip_width_mm = self.label_strip.get_total_width()
        strip_height_mm = self.label_strip.height
        width_px = int(strip_width_mm * self.scale_factor)
        height_px = int(strip_height_mm * self.scale_factor)

        pixmap = QPixmap(width_px, height_px)
        pixmap.fill(Qt.GlobalColor.white)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._draw_strip(painter, 0, 0, width_px, height_px)
        painter.end()
        return pixmap

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

            # 1 inch = 25.4 mm  →  pixels per mm = dpi / 25.4
            png_scale_factor = dpi / 25.4

            strip_width_mm = self.label_strip.get_total_width()
            strip_height_mm = self.label_strip.height
            width_px = int(strip_width_mm * png_scale_factor)
            height_px = int(strip_height_mm * png_scale_factor)

            pixmap = QPixmap(width_px, height_px)
            pixmap.fill(Qt.GlobalColor.white)

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
            self._draw_strip_scaled(painter, 0, 0, width_px, height_px, png_scale_factor)
            painter.end()

            return pixmap.save(output_path, "PNG")

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Error saving PNG: %s", e, exc_info=True)
            return False

    def _draw_strip(self, painter: QPainter, x: int, y: int, width: int, height: int) -> None:
        """Draw the strip using the default scale factor."""
        self._draw_strip_scaled(painter, x, y, width, height, self.scale_factor)

    def _draw_strip_scaled(self, painter: QPainter, x: int, y: int, _width: int, height: int, scale: float) -> None:
        """
        Draw the strip with a specific scale factor.

        Args:
            painter: QPainter to draw with
            x: X position in pixels
            y: Y position in pixels
            _width: Total width in pixels (unused; derived from segment widths)
            height: Total height in pixels
            scale: Scale factor (pixels per mm)
        """
        current_x = x

        if self.label_strip.start_segment and self.label_strip.start_segment.width > 0:
            segment_width_px = int(self.label_strip.start_segment.width * scale)
            self._draw_segment(painter, current_x, y, segment_width_px, height, self.label_strip.start_segment, scale)
            current_x += segment_width_px

        for segment in self.label_strip.content_segments:
            segment_width_px = int(segment.width * scale)
            self._draw_segment(painter, current_x, y, segment_width_px, height, segment, scale)
            current_x += segment_width_px

        if self.label_strip.end_segment and self.label_strip.end_segment.width > 0:
            segment_width_px = int(self.label_strip.end_segment.width * scale)
            self._draw_segment(painter, current_x, y, segment_width_px, height, self.label_strip.end_segment, scale)

    def _draw_segment(
        self,
        painter: QPainter,
        x: int,
        y: int,
        width: int,
        height: int,
        segment: Segment,
        scale: float,
    ) -> None:
        """
        Draw a single segment.

        Args:
            painter: QPainter to draw with
            x: X position in pixels
            y: Y position in pixels
            width: Segment width in pixels
            height: Segment height in pixels
            segment: The segment to draw
            scale: Scale factor (pixels per mm), used for font sizing
        """
        bg_color = QColor(segment.background_color.r, segment.background_color.g, segment.background_color.b)
        text_color = QColor(segment.text_color.r, segment.text_color.g, segment.text_color.b)

        painter.fillRect(x, y, width, height, bg_color)
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.drawRect(x, y, width, height)

        if segment.text:
            painter.setPen(text_color)

            # Convert pt -> px: pixels = points * (scale px/mm) * (25.4 mm/in) / (72 pt/in)
            font_size_px = int(self.label_strip.settings.default_font_size * scale * 25.4 / 72)
            font = QFont(self.label_strip.settings.default_font_name)
            font.setPixelSize(max(1, font_size_px))

            text_fmt = getattr(segment, "text_format", None)
            if text_fmt == TextFormat.BOLD:
                font.setBold(True)
            elif text_fmt == TextFormat.ITALIC:
                font.setItalic(True)
            elif text_fmt == TextFormat.BOLD_ITALIC:
                font.setBold(True)
                font.setItalic(True)

            painter.setFont(font)

            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(segment.text)
            text_height = metrics.height()

            # Horizontally centred; baseline-aware vertical centre
            text_x = x + (width - text_width) / 2
            text_y = y + (height + text_height) / 2 - metrics.descent()

            painter.drawText(int(text_x), int(text_y), segment.text)

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
        return (int(width_mm * self.scale_factor), int(height_mm * self.scale_factor))

    def get_strip_dimensions_mm(self) -> tuple[float, float]:
        """
        Get the strip dimensions in millimeters.

        Returns:
            Tuple of (width_mm, height_mm)
        """
        if not self.label_strip:
            return (0.0, 0.0)

        return (self.label_strip.get_total_width(), self.label_strip.height)
