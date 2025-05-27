"""
PDF generation utilities for label strips.
"""

from typing import ClassVar

from reportlab.lib import colors
from reportlab.lib.pagesizes import A0, A1, A2, A3, A4, LEGAL, LETTER, TABLOID
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from jackfield_labeler.models.label_strip import LabelStrip, Segment
from jackfield_labeler.models.strip_settings import PaperSize


class PDFGenerator:
    """Generates PDF documents from label strips."""

    # Paper size mapping
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

    def __init__(self, label_strip: LabelStrip):
        """
        Initialize the PDF generator.

        Args:
            label_strip: The label strip to generate PDF for
        """
        self.label_strip = label_strip
        self.settings = label_strip.settings

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
            # Use rotation from settings if not specified
            if rotation_angle is None:
                rotation_angle = self.settings.rotation_angle

            # Get paper size
            paper_size = self.PAPER_SIZES.get(self.settings.paper_size, A4)
            page_width, page_height = paper_size

            # Create the PDF canvas
            c = canvas.Canvas(output_path, pagesize=paper_size)

            # Calculate strip dimensions in points
            strip_width_mm = self.label_strip.get_total_width()
            strip_height_mm = self.label_strip.height
            strip_width_pts = strip_width_mm * mm
            strip_height_pts = strip_height_mm * mm

            # Calculate page center
            page_center_x = page_width / 2
            page_center_y = page_height / 2

            # Calculate strip center (relative to strip's origin)
            strip_center_x = strip_width_pts / 2
            strip_center_y = strip_height_pts / 2

            # Save the graphics state
            c.saveState()

            # Move to page center
            c.translate(page_center_x, page_center_y)

            # Apply rotation around the center
            c.rotate(rotation_angle)

            # Draw the strip centered at origin (which is now the page center)
            # No scaling - preserve exact dimensions
            # The strip's bottom-left corner should be at (-strip_center_x, -strip_center_y)
            strip_x = -strip_center_x
            strip_y = -strip_center_y

            self._draw_label_strip(c, strip_x, strip_y, strip_width_pts, strip_height_pts)

            # Restore the graphics state
            c.restoreState()

            # Save the PDF
            c.save()
        except Exception as e:
            print(f"Error generating PDF: {e}")
            import traceback

            traceback.print_exc()
            return False
        else:
            return True

    def _should_rotate(
        self,
        strip_width: float,
        strip_height: float,
        available_width: float,
        available_height: float,
        rotation_angle: float,
    ) -> bool:
        """
        Determine if rotation should be applied.

        Args:
            strip_width: Strip width in points
            strip_height: Strip height in points
            available_width: Available page width in points
            available_height: Available page height in points
            rotation_angle: Requested rotation angle

        Returns:
            True if rotation should be applied
        """
        # If rotation angle is specified and not 0, apply it
        if rotation_angle != 0.0:
            return True

        # Auto-rotate if strip doesn't fit without rotation but would fit with rotation
        fits_normal = strip_width <= available_width and strip_height <= available_height
        fits_rotated = strip_height <= available_width and strip_width <= available_height

        return not fits_normal and fits_rotated

    def _draw_label_strip(self, canvas_obj: canvas.Canvas, x: float, y: float, width: float, height: float) -> None:
        """
        Draw the label strip on the canvas.

        Args:
            canvas_obj: The reportlab canvas
            x: X position in points
            y: Y position in points
            width: Strip width in points
            height: Strip height in points
        """
        current_x = x

        # Draw start segment if present
        if self.label_strip.start_segment:
            segment_width = self.label_strip.start_segment.width * mm
            self._draw_segment(canvas_obj, current_x, y, segment_width, height, self.label_strip.start_segment)
            current_x += segment_width

        # Draw content segments
        for segment in self.label_strip.content_segments:
            segment_width = segment.width * mm
            self._draw_segment(canvas_obj, current_x, y, segment_width, height, segment)
            current_x += segment_width

        # Draw end segment if present
        if self.label_strip.end_segment:
            segment_width = self.label_strip.end_segment.width * mm
            self._draw_segment(canvas_obj, current_x, y, segment_width, height, self.label_strip.end_segment)

    def _draw_segment(
        self, canvas_obj: canvas.Canvas, x: float, y: float, width: float, height: float, segment: Segment
    ) -> None:
        """
        Draw a single segment.

        Args:
            canvas_obj: The reportlab canvas
            x: X position in points
            y: Y position in points
            width: Segment width in points
            height: Segment height in points
            segment: The segment to draw
        """
        # Convert colors to reportlab format
        bg_color = colors.Color(
            segment.background_color.r / 255.0,
            segment.background_color.g / 255.0,
            segment.background_color.b / 255.0,
        )

        text_color = colors.Color(
            segment.text_color.r / 255.0, segment.text_color.g / 255.0, segment.text_color.b / 255.0
        )

        # Draw background
        canvas_obj.setFillColor(bg_color)
        canvas_obj.rect(x, y, width, height, fill=1, stroke=1)

        # Draw border
        canvas_obj.setStrokeColor(colors.black)
        canvas_obj.setLineWidth(0.5)
        canvas_obj.rect(x, y, width, height, fill=0, stroke=1)

        # Draw text if present
        if segment.text:
            canvas_obj.setFillColor(text_color)

            # Set font based on text format
            font_name = "Helvetica"  # Use Helvetica as default since it's always available
            font_size = self.settings.default_font_size

            # Apply text formatting
            if hasattr(segment, "text_format") and segment.text_format:
                if segment.text_format.name == "BOLD":
                    font_name = "Helvetica-Bold"
                elif segment.text_format.name == "ITALIC":
                    font_name = "Helvetica-Oblique"

            canvas_obj.setFont(font_name, font_size)

            # Calculate text position (centered horizontally and vertically)
            text_width = canvas_obj.stringWidth(segment.text, font_name, font_size)
            text_x = x + (width - text_width) / 2
            # Center the text vertically in the cell
            text_y = y + height / 2 - font_size / 2

            canvas_obj.drawString(text_x, text_y, segment.text)

    def calculate_required_rotation(self) -> float | None:
        """
        Calculate the optimal rotation angle for the strip to fit on the page.

        Returns:
            Rotation angle in degrees (0, 90, 180, 270) or None if no rotation needed
        """
        # Get paper size
        paper_size = self.PAPER_SIZES.get(self.settings.paper_size, A4)
        page_width, page_height = paper_size

        # Calculate available space
        margin_left = self.settings.page_margins.left * mm
        margin_top = self.settings.page_margins.top * mm
        margin_right = self.settings.page_margins.right * mm
        margin_bottom = self.settings.page_margins.bottom * mm

        available_width = page_width - margin_left - margin_right
        available_height = page_height - margin_top - margin_bottom

        # Get strip dimensions
        strip_width_pts = self.label_strip.get_total_width() * mm
        strip_height_pts = self.label_strip.height * mm

        # Check if it fits without rotation
        if strip_width_pts <= available_width and strip_height_pts <= available_height:
            return None

        # Check if it fits with 90-degree rotation
        if strip_height_pts <= available_width and strip_width_pts <= available_height:
            return 90.0

        # If it doesn't fit either way, try rotation anyway if the strip is wider than it is tall
        # This will at least orient it better for viewing
        if strip_width_pts > strip_height_pts and strip_width_pts > available_width:
            return 90.0

        # If it doesn't fit either way, return None (will need scaling or different approach)
        return None
