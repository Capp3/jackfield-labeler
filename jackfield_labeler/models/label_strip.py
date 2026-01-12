"""
Main LabelStrip class for representing a complete label strip.
"""

import json
from typing import Any

from jackfield_labeler.models.exceptions import (
    ContentCellWidthError,
    ContentSegmentCountError,
    EndSegmentWidthError,
    StartSegmentWidthError,
)
from jackfield_labeler.models.segment import Segment
from jackfield_labeler.models.segment_types import ContentSegment, EndSegment, StartSegment, create_segment_from_dict
from jackfield_labeler.models.strip_settings import StripSettings


class LabelStrip:
    """
    Represents a complete label strip with all its segments.

    A label strip consists of:
    - An optional start segment
    - Multiple content segments (cells)
    - An optional end segment
    """

    # Constants for validation
    MIN_HEIGHT = 5.0  # mm
    MAX_HEIGHT = 12.0  # mm
    MAX_WIDTH = 500.0  # mm

    def __init__(self, height: float = 5.0):
        """
        Initialize a new label strip.

        Args:
            height: The height of the strip in mm (default: 5.0)
        """
        self._height = max(self.MIN_HEIGHT, min(height, self.MAX_HEIGHT))
        self._start_segment: StartSegment | None = None
        self._end_segment: EndSegment | None = None
        self._content_segments: list[ContentSegment] = []
        self._content_cell_width: float = 10.0  # Default in mm
        self._settings = StripSettings()

    @property
    def height(self) -> float:
        """Get the height of the strip in mm."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """
        Set the height of the strip in mm.

        The height is constrained to the allowed range.

        Args:
            value: Height in mm
        """
        self._height = max(self.MIN_HEIGHT, min(value, self.MAX_HEIGHT))

    @property
    def content_cell_width(self) -> float:
        """Get the width of content cells in mm."""
        return self._content_cell_width

    @content_cell_width.setter
    def content_cell_width(self, value: float) -> None:
        """
        Set the width of content cells in mm.

        Args:
            value: Width in mm

        Raises:
            ContentCellWidthError: If the width is not positive
        """
        if value <= 0:
            raise ContentCellWidthError()

        # Round to 3 decimal places for practical precision
        self._content_cell_width = round(value, 3)

        # Update all content segments with the new width
        for segment in self._content_segments:
            segment.width = self._content_cell_width

    @property
    def start_segment(self) -> StartSegment | None:
        """Get the start segment, or None if not used."""
        return self._start_segment

    @property
    def end_segment(self) -> EndSegment | None:
        """Get the end segment, or None if not used."""
        return self._end_segment

    @property
    def content_segments(self) -> list[ContentSegment]:
        """Get a copy of the list of content segments."""
        return self._content_segments.copy()

    @property
    def settings(self) -> StripSettings:
        """Get the strip settings."""
        return self._settings

    @settings.setter
    def settings(self, value: StripSettings) -> None:
        """Set the strip settings."""
        self._settings = value

    def set_start_segment(self, width: float = 0.0, text: str = "") -> StartSegment | None:
        """
        Configure the start segment of the strip.

        Args:
            width: Width in mm (0.0 means no start segment)
            text: Text content

        Returns:
            The start segment instance

        Raises:
            StartSegmentWidthError: If the width is negative
        """
        if width < 0:
            raise StartSegmentWidthError()

        if width > 0:
            if self._start_segment is None:
                self._start_segment = StartSegment(
                    width=width,
                    text=text,
                    text_color=self._settings.default_text_color,
                    background_color=self._settings.default_background_color,
                )
            else:
                self._start_segment.width = width
                self._start_segment.text = text
        else:
            # Width is 0, effectively removing the start segment
            self._start_segment = None

        return self._start_segment

    def set_end_segment(self, width: float = 0.0, text: str = "") -> EndSegment | None:
        """
        Configure the end segment of the strip.

        Args:
            width: Width in mm (0.0 means no end segment)
            text: Text content

        Returns:
            The end segment instance

        Raises:
            EndSegmentWidthError: If the width is negative
        """
        if width < 0:
            raise EndSegmentWidthError()

        if width > 0:
            if self._end_segment is None:
                self._end_segment = EndSegment(
                    width=width,
                    text=text,
                    text_color=self._settings.default_text_color,
                    background_color=self._settings.default_background_color,
                )
            else:
                self._end_segment.width = width
                self._end_segment.text = text
        else:
            # Width is 0, effectively removing the end segment
            self._end_segment = None

        return self._end_segment

    def set_content_segment_count(self, count: int) -> None:
        """
        Set the number of content segments.

        This will add or remove segments as needed.

        Args:
            count: Number of content segments

        Raises:
            ContentSegmentCountError: If count is negative
        """
        if count < 0:
            raise ContentSegmentCountError()

        current_count = len(self._content_segments)

        if count > current_count:
            # Add new segments
            for i in range(current_count, count):
                segment_id = str(i + 1)  # 1-based IDs for user-facing segments
                self._content_segments.append(
                    ContentSegment(
                        segment_id=segment_id,
                        width=self._content_cell_width,
                        text_color=self._settings.default_text_color,
                        background_color=self._settings.default_background_color,
                    )
                )
        elif count < current_count:
            # Remove excess segments
            self._content_segments = self._content_segments[:count]

    def get_all_segments(self) -> list[Segment]:
        """
        Get a list of all segments in order.

        Returns:
            List of segments (start, content, end)
        """
        result: list[Segment] = []

        if self._start_segment is not None:
            result.append(self._start_segment)

        result.extend(self._content_segments)

        if self._end_segment is not None:
            result.append(self._end_segment)

        return result

    def get_total_width(self) -> float:
        """
        Calculate the total width of the strip in mm.

        Returns:
            Total width in mm
        """
        total = 0.0

        if self._start_segment is not None:
            total += self._start_segment.width

        total += len(self._content_segments) * self._content_cell_width

        if self._end_segment is not None:
            total += self._end_segment.width

        return total

    def get_segment_by_id(self, segment_id: str) -> Segment | None:
        """
        Find a segment by its ID.

        Args:
            segment_id: Segment ID to find

        Returns:
            The segment if found, otherwise None
        """
        if self._start_segment is not None and self._start_segment.id == segment_id:
            return self._start_segment

        for segment in self._content_segments:
            if segment.id == segment_id:
                return segment

        if self._end_segment is not None and self._end_segment.id == segment_id:
            return self._end_segment

        return None

    def validate(self) -> list[str]:
        """
        Validate the strip configuration.

        Returns:
            List of validation error messages, or an empty list if valid
        """
        errors = []

        # Check height
        if self._height < self.MIN_HEIGHT:
            errors.append(f"Strip height ({self._height} mm) is below minimum ({self.MIN_HEIGHT} mm)")
        elif self._height > self.MAX_HEIGHT:
            errors.append(f"Strip height ({self._height} mm) exceeds maximum ({self.MAX_HEIGHT} mm)")

        # Check content cell width
        if self._content_cell_width <= 0:
            errors.append("Content cell width must be positive")

        # Check start segment
        if self._start_segment is not None and self._start_segment.width < 0:
            errors.append("Start segment width cannot be negative")

        # Check end segment
        if self._end_segment is not None and self._end_segment.width < 0:
            errors.append("End segment width cannot be negative")

        # Check total width
        total_width = self.get_total_width()
        if total_width > self.MAX_WIDTH:
            errors.append(f"Total strip width ({total_width} mm) exceeds maximum ({self.MAX_WIDTH} mm)")
        elif total_width <= 0:
            errors.append("Strip has zero or negative width")

        return errors

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the label strip to a dictionary for serialization.

        Returns:
            Dictionary representation of the label strip
        """
        segments = []
        if self._start_segment is not None:
            segments.append(self._start_segment.to_dict())

        for segment in self._content_segments:
            segments.append(segment.to_dict())

        if self._end_segment is not None:
            segments.append(self._end_segment.to_dict())

        return {
            "height": self._height,
            "content_cell_width": self._content_cell_width,
            "segments": segments,
            "settings": self._settings.to_dict(),
        }

    def to_json(self) -> str:
        """
        Convert the label strip to a JSON string.

        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LabelStrip":
        """
        Create a label strip from a dictionary representation.

        Args:
            data: Dictionary containing label strip data

        Returns:
            A new LabelStrip instance
        """
        strip = cls(height=data.get("height", 5.0))
        strip._content_cell_width = data.get("content_cell_width", 10.0)

        # Load settings if present
        if "settings" in data:
            strip._settings = StripSettings.from_dict(data["settings"])

        # Load segments
        segments_data = data.get("segments", [])
        content_segments: list[ContentSegment] = []

        for segment_data in segments_data:
            segment = create_segment_from_dict(segment_data)
            segment_type = segment_data.get("type", "").lower()

            if segment_type == "start":
                if not isinstance(segment, StartSegment):
                    raise TypeError(f"Expected StartSegment, got {type(segment).__name__}")
                strip._start_segment = segment
            elif segment_type == "end":
                if not isinstance(segment, EndSegment):
                    raise TypeError(f"Expected EndSegment, got {type(segment).__name__}")
                strip._end_segment = segment
            elif segment_type == "content":
                if not isinstance(segment, ContentSegment):
                    raise TypeError(f"Expected ContentSegment, got {type(segment).__name__}")
                content_segments.append(segment)

        strip._content_segments = content_segments
        return strip

    @classmethod
    def from_json(cls, json_str: str) -> "LabelStrip":
        """
        Create a label strip from a JSON string.

        Args:
            json_str: JSON string representation

        Returns:
            A new LabelStrip instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
