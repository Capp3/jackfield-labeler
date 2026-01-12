"""
Concrete segment type implementations for label strips.
"""

from typing import Any

from jackfield_labeler.models.color import BLACK, WHITE, Color
from jackfield_labeler.models.exceptions import UnknownSegmentTypeError
from jackfield_labeler.models.segment import Segment
from jackfield_labeler.models.text_format import TextFormat


class StartSegment(Segment):
    """
    Represents the optional starting segment of a label strip.
    """

    def __init__(
        self,
        width: float = 0.0,
        text: str = "",
        text_format: TextFormat = TextFormat.NORMAL,
        text_color: Color = BLACK,
        background_color: Color = WHITE,
    ):
        """
        Initialize a start segment.

        Args:
            width: Width of the segment in mm
            text: Text content of the segment
            text_format: Formatting to apply to the text
            text_color: Color for the text
            background_color: Background color for the segment
        """
        super().__init__(
            segment_id="L_START",
            text=text,
            width=width,
            text_format=text_format,
            text_color=text_color,
            background_color=background_color,
        )

    def get_type(self) -> str:
        """Return the type of segment as a string."""
        return "start"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StartSegment":
        """
        Create a StartSegment from a dictionary representation.

        Args:
            data: Dictionary containing segment data

        Returns:
            A new StartSegment instance
        """
        text_format_str = data.get("text_format", "NORMAL").upper()
        try:
            text_format = TextFormat[text_format_str]
        except KeyError:
            text_format = TextFormat.NORMAL

        return cls(
            width=data.get("width", 0.0),
            text=data.get("text", ""),
            text_format=text_format,
            text_color=Color.from_hex(data.get("text_color", "#000000")),
            background_color=Color.from_hex(data.get("background_color", "#FFFFFF")),
        )


class ContentSegment(Segment):
    """
    Represents a content cell segment within a label strip.
    """

    def __init__(
        self,
        segment_id: str,
        width: float,
        text: str = "",
        text_format: TextFormat = TextFormat.NORMAL,
        text_color: Color = BLACK,
        background_color: Color = WHITE,
    ):
        """
        Initialize a content segment.

        Args:
            segment_id: Unique identifier for this segment (typically a number)
            width: Width of the segment in mm
            text: Text content of the segment
            text_format: Formatting to apply to the text
            text_color: Color for the text
            background_color: Background color for the segment
        """
        super().__init__(
            segment_id=segment_id,
            text=text,
            width=width,
            text_format=text_format,
            text_color=text_color,
            background_color=background_color,
        )

    def get_type(self) -> str:
        """Return the type of segment as a string."""
        return "content"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContentSegment":
        """
        Create a ContentSegment from a dictionary representation.

        Args:
            data: Dictionary containing segment data

        Returns:
            A new ContentSegment instance
        """
        text_format_str = data.get("text_format", "NORMAL").upper()
        try:
            text_format = TextFormat[text_format_str]
        except KeyError:
            text_format = TextFormat.NORMAL

        return cls(
            segment_id=data.get("id", "0"),
            width=data.get("width", 10.0),
            text=data.get("text", ""),
            text_format=text_format,
            text_color=Color.from_hex(data.get("text_color", "#000000")),
            background_color=Color.from_hex(data.get("background_color", "#FFFFFF")),
        )


class EndSegment(Segment):
    """
    Represents the optional ending segment of a label strip.
    """

    def __init__(
        self,
        width: float = 0.0,
        text: str = "",
        text_format: TextFormat = TextFormat.NORMAL,
        text_color: Color = BLACK,
        background_color: Color = WHITE,
    ):
        """
        Initialize an end segment.

        Args:
            width: Width of the segment in mm
            text: Text content of the segment
            text_format: Formatting to apply to the text
            text_color: Color for the text
            background_color: Background color for the segment
        """
        super().__init__(
            segment_id="L_END",
            text=text,
            width=width,
            text_format=text_format,
            text_color=text_color,
            background_color=background_color,
        )

    def get_type(self) -> str:
        """Return the type of segment as a string."""
        return "end"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EndSegment":
        """
        Create an EndSegment from a dictionary representation.

        Args:
            data: Dictionary containing segment data

        Returns:
            A new EndSegment instance
        """
        text_format_str = data.get("text_format", "NORMAL").upper()
        try:
            text_format = TextFormat[text_format_str]
        except KeyError:
            text_format = TextFormat.NORMAL

        return cls(
            width=data.get("width", 0.0),
            text=data.get("text", ""),
            text_format=text_format,
            text_color=Color.from_hex(data.get("text_color", "#000000")),
            background_color=Color.from_hex(data.get("background_color", "#FFFFFF")),
        )


# Factory function for creating segments from serialized data
def create_segment_from_dict(data: dict[str, Any]) -> Segment:
    """
    Factory function to create the appropriate segment type from dictionary data.

    Args:
        data: Dictionary containing segment data including 'type'

    Returns:
        A Segment instance of the appropriate subclass

    Raises:
        UnknownSegmentTypeError: If the segment type is not recognized
    """
    segment_type = data.get("type", "").lower()

    if segment_type == "start":
        return StartSegment.from_dict(data)
    if segment_type == "content":
        return ContentSegment.from_dict(data)
    if segment_type == "end":
        return EndSegment.from_dict(data)
    raise UnknownSegmentTypeError(segment_type)
