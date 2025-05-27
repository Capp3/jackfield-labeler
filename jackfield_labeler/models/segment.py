"""
Base segment class and related definitions for label strips.
"""

from abc import ABC, abstractmethod
from typing import Any

from jackfield_labeler.models.color import BLACK, WHITE, Color
from jackfield_labeler.models.exceptions import SegmentWidthError
from jackfield_labeler.models.text_format import TextFormat


class Segment(ABC):
    """
    Abstract base class for all segment types in a label strip.
    """

    def __init__(
        self,
        segment_id: str,
        text: str = "",
        width: float = 0.0,
        text_format: TextFormat = TextFormat.NORMAL,
        text_color: Color = BLACK,
        background_color: Color = WHITE,
    ):
        """
        Initialize a new segment.

        Args:
            segment_id: Unique identifier for this segment
            text: Text content of the segment
            width: Width of the segment in mm
            text_format: Formatting to apply to the text
            text_color: Color for the text
            background_color: Background color for the segment
        """
        self._id = segment_id
        self._text = text
        self._width = width
        self._text_format = text_format
        self._text_color = text_color
        self._background_color = background_color

    @property
    def id(self) -> str:
        """Get the segment's unique identifier."""
        return self._id

    @property
    def text(self) -> str:
        """Get the segment's text content."""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        """Set the segment's text content."""
        self._text = value

    @property
    def width(self) -> float:
        """Get the segment's width in mm."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Set the segment's width in mm."""
        if value < 0:
            raise SegmentWidthError()

        # Round to 3 decimal places for practical precision
        self._width = round(value, 3)

    @property
    def text_format(self) -> TextFormat:
        """Get the segment's text format."""
        return self._text_format

    @text_format.setter
    def text_format(self, value: TextFormat) -> None:
        """Set the segment's text format."""
        self._text_format = value

    @property
    def text_color(self) -> Color:
        """Get the segment's text color."""
        return self._text_color

    @text_color.setter
    def text_color(self, value: Color) -> None:
        """Set the segment's text color."""
        self._text_color = value

    @property
    def background_color(self) -> Color:
        """Get the segment's background color."""
        return self._background_color

    @background_color.setter
    def background_color(self, value: Color) -> None:
        """Set the segment's background color."""
        self._background_color = value

    @abstractmethod
    def get_type(self) -> str:
        """Return the type of segment as a string."""
        pass

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the segment to a dictionary for serialization.

        Returns:
            Dictionary representation of the segment
        """
        return {
            "id": self._id,
            "type": self.get_type(),
            "text": self._text,
            "width": self._width,
            "text_format": self._text_format.name,
            "text_color": self._text_color.to_hex(),
            "background_color": self._background_color.to_hex(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Segment":
        """
        Create a segment from a dictionary representation.
        This method should be implemented by subclasses.

        Args:
            data: Dictionary containing segment data

        Returns:
            A new Segment instance
        """
        raise NotImplementedError("Subclasses must implement from_dict")
