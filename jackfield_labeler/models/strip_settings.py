"""
Settings for label strips, including global preferences.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from jackfield_labeler.models.color import BLACK, WHITE, Color


class PaperSize(Enum):
    """Standard paper sizes."""

    A4 = "A4"
    A3 = "A3"
    A2 = "A2"
    A1 = "A1"
    A0 = "A0"
    LETTER = "Letter"
    LEGAL = "Legal"
    TABLOID = "Tabloid"

    def __str__(self) -> str:
        """Return a string representation."""
        return self.value


@dataclass
class PageMargins:
    """Page margins for printing."""

    top: float = 10.0  # mm
    right: float = 10.0  # mm
    bottom: float = 10.0  # mm
    left: float = 10.0  # mm


@dataclass
class StripSettings:
    """
    Global settings for label strips.

    These settings apply to all strips and affect PDF generation.
    """

    # Paper settings
    paper_size: PaperSize = PaperSize.A4
    page_margins: PageMargins = field(default_factory=PageMargins)

    # Default formatting
    default_font_name: str = "Arial"
    default_font_size: float = 8.0  # pt
    default_text_color: Color = BLACK
    default_background_color: Color = WHITE

    def to_dict(self) -> dict[str, Any]:
        """
        Convert settings to a dictionary for serialization.

        Returns:
            Dictionary representation of settings
        """
        return {
            "paper_size": self.paper_size.value,
            "page_margins": {
                "top": self.page_margins.top,
                "right": self.page_margins.right,
                "bottom": self.page_margins.bottom,
                "left": self.page_margins.left,
            },
            "default_font_name": self.default_font_name,
            "default_font_size": self.default_font_size,
            "default_text_color": self.default_text_color.to_hex(),
            "default_background_color": self.default_background_color.to_hex(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StripSettings":
        """
        Create settings from a dictionary representation.

        Args:
            data: Dictionary containing settings

        Returns:
            A new StripSettings instance
        """
        margins_data = data.get("page_margins", {})
        margins = PageMargins(
            top=margins_data.get("top", 10.0),
            right=margins_data.get("right", 10.0),
            bottom=margins_data.get("bottom", 10.0),
            left=margins_data.get("left", 10.0),
        )

        return cls(
            paper_size=PaperSize(data.get("paper_size", "A4")),
            page_margins=margins,
            default_font_name=data.get("default_font_name", "Arial"),
            default_font_size=data.get("default_font_size", 8.0),
            default_text_color=Color.from_hex(data.get("default_text_color", "#000000")),
            default_background_color=Color.from_hex(data.get("default_background_color", "#FFFFFF")),
        )
