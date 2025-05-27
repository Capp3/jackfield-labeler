"""
Custom exceptions for the jackfield_labeler package.
"""


class ContentCellWidthError(ValueError):
    """Raised when content cell width is not positive."""

    def __init__(self):
        super().__init__("Content cell width must be positive")


class SegmentWidthError(ValueError):
    """Raised when segment width is negative."""

    def __init__(self):
        super().__init__("Segment width cannot be negative")


class StartSegmentWidthError(ValueError):
    """Raised when start segment width is negative."""

    def __init__(self):
        super().__init__("Start segment width cannot be negative")


class EndSegmentWidthError(ValueError):
    """Raised when end segment width is negative."""

    def __init__(self):
        super().__init__("End segment width cannot be negative")


class ContentSegmentCountError(ValueError):
    """Raised when content segment count is negative."""

    def __init__(self):
        super().__init__("Content segment count cannot be negative")


class UnknownSegmentTypeError(ValueError):
    """Raised when an unknown segment type is encountered."""

    def __init__(self, segment_type):
        super().__init__(f"Unknown segment type: {segment_type}")
