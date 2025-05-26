"""
Tests for the Label Strip data model.
"""

from jackfield_labeler.models import Color, LabelStrip, TextFormat


def test_label_strip_init():
    """Test basic initialization of a label strip."""
    strip = LabelStrip()
    assert strip.height == 5.0
    assert strip.content_cell_width == 10.0
    assert strip.start_segment is None
    assert strip.end_segment is None
    assert len(strip.content_segments) == 0


def test_label_strip_height_constraints():
    """Test height constraints are enforced."""
    # Test minimum height
    strip = LabelStrip(height=1.0)  # Too small, should be set to minimum
    assert strip.height == LabelStrip.MIN_HEIGHT

    # Test maximum height
    strip = LabelStrip(height=20.0)  # Too large, should be set to maximum
    assert strip.height == LabelStrip.MAX_HEIGHT

    # Test valid height
    strip = LabelStrip(height=8.5)
    assert strip.height == 8.5


def test_content_segments():
    """Test adding and manipulating content segments."""
    strip = LabelStrip()

    # Add content segments
    strip.set_content_segment_count(3)
    assert len(strip.content_segments) == 3

    # Check segment IDs
    segments = strip.content_segments
    assert segments[0].id == "1"
    assert segments[1].id == "2"
    assert segments[2].id == "3"

    # Check segment widths
    for segment in segments:
        assert segment.width == strip.content_cell_width

    # Update content cell width
    strip.content_cell_width = 15.0
    for segment in strip.content_segments:
        assert segment.width == 15.0

    # Reduce segment count
    strip.set_content_segment_count(1)
    assert len(strip.content_segments) == 1
    assert strip.content_segments[0].id == "1"


def test_start_end_segments():
    """Test manipulating start and end segments."""
    strip = LabelStrip()

    # Initially no start/end segments
    assert strip.start_segment is None
    assert strip.end_segment is None

    # Add start segment
    start = strip.set_start_segment(width=20.0, text="Start")
    assert strip.start_segment is not None
    assert strip.start_segment.width == 20.0
    assert strip.start_segment.text == "Start"
    assert start is strip.start_segment

    # Add end segment
    end = strip.set_end_segment(width=15.0, text="End")
    assert strip.end_segment is not None
    assert strip.end_segment.width == 15.0
    assert strip.end_segment.text == "End"
    assert end is strip.end_segment

    # Remove start segment
    strip.set_start_segment(0.0)
    assert strip.start_segment is None

    # Remove end segment
    strip.set_end_segment(0.0)
    assert strip.end_segment is None


def test_total_width_calculation():
    """Test the total width calculation."""
    strip = LabelStrip()

    # Empty strip
    assert strip.get_total_width() == 0.0

    # Add content segments
    strip.set_content_segment_count(2)
    assert strip.get_total_width() == 2 * strip.content_cell_width

    # Add start segment
    strip.set_start_segment(width=15.0)
    assert strip.get_total_width() == 15.0 + 2 * strip.content_cell_width

    # Add end segment
    strip.set_end_segment(width=10.0)
    assert strip.get_total_width() == 15.0 + 2 * strip.content_cell_width + 10.0


def test_validation():
    """Test strip validation."""
    strip = LabelStrip()

    # Empty strip should have errors
    errors = strip.validate()
    assert len(errors) > 0
    assert any("zero or negative width" in error for error in errors)

    # Add content segments to fix width error
    strip.set_content_segment_count(2)
    errors = strip.validate()
    assert len(errors) == 0

    # Add excessive width
    strip.content_cell_width = 300
    strip.set_content_segment_count(2)
    errors = strip.validate()
    assert len(errors) > 0
    assert any("exceeds maximum" in error for error in errors)


def test_serialization():
    """Test serialization to and from dict/JSON."""
    # Create a strip with various segments
    strip = LabelStrip(height=7.5)
    strip.content_cell_width = 12.5
    strip.set_content_segment_count(3)
    strip.set_start_segment(width=20.0, text="Start")
    strip.set_end_segment(width=15.0, text="End")

    # Add some formatting to segments
    strip.start_segment.text_format = TextFormat.BOLD
    strip.content_segments[1].text = "Middle"
    strip.content_segments[1].background_color = Color(255, 0, 0)  # Red background

    # Convert to dict
    data = strip.to_dict()

    # Check basic properties
    assert data["height"] == 7.5
    assert data["content_cell_width"] == 12.5

    # Check segments
    assert len(data["segments"]) == 5  # start + 3 content + end
    assert data["segments"][0]["type"] == "start"
    assert data["segments"][-1]["type"] == "end"
    assert data["segments"][2]["text"] == "Middle"

    # Round-trip through JSON
    json_str = strip.to_json()
    new_strip = LabelStrip.from_json(json_str)

    # Check properties were preserved
    assert new_strip.height == 7.5
    assert new_strip.content_cell_width == 12.5
    assert new_strip.start_segment is not None
    assert new_strip.start_segment.width == 20.0
    assert new_strip.start_segment.text == "Start"
    assert new_strip.start_segment.text_format == TextFormat.BOLD
    assert len(new_strip.content_segments) == 3
    assert new_strip.content_segments[1].text == "Middle"
    assert new_strip.content_segments[1].background_color.r == 255
    assert new_strip.content_segments[1].background_color.g == 0
    assert new_strip.content_segments[1].background_color.b == 0
    assert new_strip.end_segment is not None
    assert new_strip.end_segment.width == 15.0
    assert new_strip.end_segment.text == "End"
