"""
Color representation for label segments.
"""

from dataclasses import dataclass
from enum import Enum


class StandardColor(Enum):
    """Standard color options for segments."""

    WHITE = "#FFFFFF"
    BLACK = "#000000"
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    YELLOW = "#FFFF00"
    ORANGE = "#FFA500"
    PURPLE = "#800080"


@dataclass
class Color:
    """
    Represents a color for use in segment text or background.
    Can be initialized with either RGB values or a hex string.
    """

    r: int = 0
    g: int = 0
    b: int = 0

    @classmethod
    def from_hex(cls, hex_color: str) -> "Color":
        """
        Create a Color from a hex string (e.g., "#FF0000").

        Args:
            hex_color: Hex color string (with or without #)

        Returns:
            A new Color instance
        """
        hex_color = hex_color.lstrip("#")
        return cls(
            r=int(hex_color[0:2], 16),
            g=int(hex_color[2:4], 16),
            b=int(hex_color[4:6], 16),
        )

    @classmethod
    def from_standard(cls, standard_color: StandardColor) -> "Color":
        """
        Create a Color from a StandardColor enum value.

        Args:
            standard_color: A StandardColor enum value

        Returns:
            A new Color instance
        """
        return cls.from_hex(standard_color.value)

    def to_hex(self) -> str:
        """
        Convert the color to a hex string.

        Returns:
            Hex color string with leading #
        """
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def to_rgb_tuple(self) -> tuple[int, int, int]:
        """
        Convert the color to an RGB tuple.

        Returns:
            (r, g, b) tuple with values from 0-255
        """
        return (self.r, self.g, self.b)

    def __str__(self) -> str:
        """Return a string representation of the color."""
        return self.to_hex()


# Common color instances
BLACK = Color.from_standard(StandardColor.BLACK)
WHITE = Color.from_standard(StandardColor.WHITE)
RED = Color.from_standard(StandardColor.RED)
GREEN = Color.from_standard(StandardColor.GREEN)
BLUE = Color.from_standard(StandardColor.BLUE)
YELLOW = Color.from_standard(StandardColor.YELLOW)
ORANGE = Color.from_standard(StandardColor.ORANGE)
PURPLE = Color.from_standard(StandardColor.PURPLE)
