"""
Models package for the jackfield labeler application.
Contains data structures and business logic.
"""

from jackfield_labeler.models.color import BLACK, BLUE, GREEN, ORANGE, PURPLE, RED, WHITE, YELLOW, Color, StandardColor
from jackfield_labeler.models.exceptions import (
    ContentCellWidthError,
    ContentSegmentCountError,
    EndSegmentWidthError,
    SegmentWidthError,
    StartSegmentWidthError,
    UnknownSegmentTypeError,
)
from jackfield_labeler.models.label_strip import LabelStrip
from jackfield_labeler.models.segment import Segment
from jackfield_labeler.models.segment_types import ContentSegment, EndSegment, StartSegment, create_segment_from_dict
from jackfield_labeler.models.strip_settings import PageMargins, PaperSize, StripSettings
from jackfield_labeler.models.text_format import TextFormat

__all__ = [
    "BLACK",
    "BLUE",
    "GREEN",
    "ORANGE",
    "PURPLE",
    "RED",
    "WHITE",
    "YELLOW",
    "Color",
    "ContentCellWidthError",
    "ContentSegment",
    "ContentSegmentCountError",
    "EndSegment",
    "EndSegmentWidthError",
    "LabelStrip",
    "PageMargins",
    "PaperSize",
    "Segment",
    "SegmentWidthError",
    "StandardColor",
    "StartSegment",
    "StartSegmentWidthError",
    "StripSettings",
    "TextFormat",
    "UnknownSegmentTypeError",
    "create_segment_from_dict",
]
