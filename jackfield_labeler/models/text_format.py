"""
Text formatting options for label segments.
"""

from enum import Enum, auto


class TextFormat(Enum):
    """Enumeration of available text formatting options."""

    NORMAL = auto()
    BOLD = auto()
    ITALIC = auto()
    BOLD_ITALIC = auto()

    def __str__(self) -> str:
        """Return a human-readable representation of the format."""
        return self.name.replace("_", " ").title()
