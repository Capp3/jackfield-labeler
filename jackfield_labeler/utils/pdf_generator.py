"""
PDF generation utilities for label strips.
"""

from typing import ClassVar

from reportlab.lib import colors
from reportlab.lib.pagesizes import A0, A1, A2, A3, A4, LEGAL, LETTER, TABLOID
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from jackfield_labeler.models.label_strip import LabelStrip
from jackfield_labeler.models.segment import Segment
from jackfield_labeler.models.strip_settings import PaperSize
from jackfield_labeler.models.text_format import TextFormat
from jackfield_labeler.utils.logger import get_logger

logger = get_logger(__name__)


class PDFGenerator:
    """Generates PDF documents from label strips."""

    # Paper size mapping (ReportLab page sizes are in points)
    PAPER_SIZES: ClassVar[dict] = {
        PaperSize.A4: A4,
        PaperSize.A3: A3,
        PaperSize.A2: A2,
        PaperSize.A1: A1,
        PaperSize.A0: A0,
        PaperSize.LETTER: LETTER,
        PaperSize.LEGAL: LEGAL,
        PaperSize.TABLOID: TABLOID,
    }

    # Map common system font names to built-in ReportLab/PDF Type1 font families.
    # Each entry maps a font family name to (normal, bold, italic, bold-italic).
    _FONT_FAMILY_MAP: ClassVar[dict[str, tuple[str, str, str, str]]] = {
        "Arial": ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique"),
        "Helvetica": ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique"),
        "Times New Roman": ("Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic"),
        "Times": ("Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic"),
        "Courier New": ("Courier", "Courier-Bold", "Courier-Oblique", "Courier-BoldOblique"),
        "Courier": ("Courier", "Courier-Bold", "Courier-Oblique", "Courier-BoldOblique"),
    }
    _DEFAULT_FAMILY: ClassVar[tuple[str, str, str, str]] = (
        "Helvetica",
        "Helvetica-Bold",
        "Helvetica-Oblique",
        "Helvetica-BoldOblique",
    )

    def __init__(self, label_strip: LabelStrip):
        """
        Initialize the PDF generator.

        Args:
            label_strip: The label strip to generate PDF for
        """
        self.label_strip = label_strip
        self.settings = label_strip.settings

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_pdf(self, output_path: str, rotation_angle: float | None = None) -> bool:
        """
        Generate a PDF file from the label strip.

        Args:
            output_path: Path where the PDF should be saved
            rotation_angle: Rotation angle in degrees (if None, uses settings rotation)

        Returns:
            True if PDF was generated successfully, False otherwise
        """
        try:
            if rotation_angle is None:
                rotation_angle = self.settings.rotation_angle

            paper_size = self.PAPER_SIZES.get(self.settings.paper_size, A4)
            page_width, page_height = paper_size

            c = canvas.Canvas(output_path, pagesize=paper_size)

            # Strip dimensions in ReportLab points
            strip_width_pts = self.label_strip.get_total_width() * mm
            strip_height_pts = self.label_strip.height * mm

            # Centre within the printable area (margins applied)
            margin_left = self.settings.page_margins.left * mm
            margin_right = self.settings.page_margins.right * mm
            margin_bottom = self.settings.page_margins.bottom * mm
            margin_top = self.settings.page_margins.top * mm

            available_width = page_width - margin_left - margin_right
            available_height = page_height - margin_bottom - margin_top

            # Centre of the printable area (ReportLab origin is bottom-left)
            center_x = margin_left + available_width / 2
            center_y = margin_bottom + available_height / 2

            c.saveState()
            c.translate(center_x, center_y)
            c.rotate(rotation_angle)

            # Draw strip centred at the (now-translated) origin
            strip_x = -strip_width_pts / 2
            strip_y = -strip_height_pts / 2
            self._draw_label_strip(c, strip_x, strip_y, strip_width_pts, strip_height_pts)

            c.restoreState()
            c.save()

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Error generating PDF: %s", e, exc_info=True)
            return False
        return True

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _resolve_font(self, text_format: TextFormat) -> str:
        """Return the ReportLab font name for the configured font and format."""
        family = self._FONT_FAMILY_MAP.get(self.settings.default_font_name, self._DEFAULT_FAMILY)
        if text_format == TextFormat.BOLD:
            return family[1]
        if text_format == TextFormat.ITALIC:
            return family[2]
        if text_format == TextFormat.BOLD_ITALIC:
            return family[3]
        return family[0]

    def _draw_label_strip(
        self,
        canvas_obj: canvas.Canvas,
        x: float,
        y: float,
        _width: float,
        height: float,
    ) -> None:
        """Draw all segments of the label strip on the canvas."""
        current_x = x

        if self.label_strip.start_segment:
            seg_w = self.label_strip.start_segment.width * mm
            self._draw_segment(canvas_obj, current_x, y, seg_w, height, self.label_strip.start_segment)
            current_x += seg_w

        for segment in self.label_strip.content_segments:
            seg_w = segment.width * mm
            self._draw_segment(canvas_obj, current_x, y, seg_w, height, segment)
            current_x += seg_w

        if self.label_strip.end_segment:
            seg_w = self.label_strip.end_segment.width * mm
            self._draw_segment(canvas_obj, current_x, y, seg_w, height, self.label_strip.end_segment)

    def _draw_segment(
        self,
        canvas_obj: canvas.Canvas,
        x: float,
        y: float,
        width: float,
        height: float,
        segment: Segment,
    ) -> None:
        """Draw a single segment (background, border, and text)."""
        bg_color = colors.Color(
            segment.background_color.r / 255.0,
            segment.background_color.g / 255.0,
            segment.background_color.b / 255.0,
        )
        text_color = colors.Color(
            segment.text_color.r / 255.0,
            segment.text_color.g / 255.0,
            segment.text_color.b / 255.0,
        )

        # Background fill + thin border
        canvas_obj.setFillColor(bg_color)
        canvas_obj.setStrokeColor(colors.black)
        canvas_obj.setLineWidth(0.5)
        canvas_obj.rect(x, y, width, height, fill=1, stroke=1)

        if not segment.text:
            return

        canvas_obj.setFillColor(text_color)

        text_fmt = getattr(segment, "text_format", TextFormat.NORMAL) or TextFormat.NORMAL
        font_name = self._resolve_font(text_fmt)
        font_size = self.settings.default_font_size

        canvas_obj.setFont(font_name, font_size)

        # Horizontal centre
        text_width = canvas_obj.stringWidth(segment.text, font_name, font_size)
        text_x = x + (width - text_width) / 2

        # Vertical centre using proper font metrics (ascent/descent in points)
        ascent, descent = pdfmetrics.getAscentDescent(font_name, font_size)
        # ascent > 0, descent < 0; cap-height approximation: centre the text block
        text_block_height = ascent - descent
        text_y = y + (height - text_block_height) / 2 - descent

        canvas_obj.drawString(text_x, text_y, segment.text)
