#!/usr/bin/env python3
"""
Test script for preview renderer and PNG export functionality.
"""

import os
import sys
from pathlib import Path

import pytest

# Add the project root to the Python path before any project imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Check if we're in a CI environment
CI_ENV = os.environ.get("CI", "false").lower() == "true"

# Skip all tests in this file when running in CI
pytestmark = pytest.mark.skipif(CI_ENV, reason="Skipping PyQt6 GUI tests in CI environment due to Qt rendering issues")

# Now we can import from the project
from PyQt6.QtWidgets import QApplication  # noqa: E402

from jackfield_labeler.models import Color, LabelStrip  # noqa: E402
from jackfield_labeler.utils.strip_renderer import StripRenderer  # noqa: E402

# Create a single QApplication instance for all tests
if "QApplication" not in globals():
    app = QApplication.instance() or QApplication(sys.argv)


# Set up temporary directory for output files
@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary directory for output files."""
    return tmp_path


def test_strip_renderer(temp_output_dir):
    """Test the strip renderer functionality."""
    # Create a test strip
    strip = LabelStrip(height=6.0)

    # Set up content segments
    strip.set_content_segment_count(4)
    strip.content_cell_width = 15.0

    # Get the segments and update their text and colors
    segments = strip.content_segments
    if len(segments) >= 4:
        segments[0].text = "IN 1"
        segments[0].background_color = Color(255, 255, 255)  # White
        segments[0].text_color = Color(0, 0, 0)  # Black

        segments[1].text = "IN 2"
        segments[1].background_color = Color(255, 200, 200)  # Light red
        segments[1].text_color = Color(0, 0, 0)  # Black

        segments[2].text = "OUT 1"
        segments[2].background_color = Color(200, 255, 200)  # Light green
        segments[2].text_color = Color(0, 0, 0)  # Black

        segments[3].text = "OUT 2"
        segments[3].background_color = Color(200, 200, 255)  # Light blue
        segments[3].text_color = Color(0, 0, 0)  # Black

    # Set end segment
    strip.set_end_segment(width=10.0, text="END")
    if strip.end_segment:
        strip.end_segment.background_color = Color(255, 255, 0)  # Yellow
        strip.end_segment.text_color = Color(0, 0, 0)  # Black

    # Test renderer creation
    renderer = StripRenderer(strip, scale_factor=10.0)

    # Test dimension calculations
    width_px, height_px = renderer.get_strip_dimensions_px()
    width_mm, height_mm = renderer.get_strip_dimensions_mm()
    assert width_px > 0
    assert height_px > 0
    assert width_mm > 0
    assert height_mm > 0

    # Test PNG export in temp directory
    png_path = temp_output_dir / "test_strip_preview.png"
    success = renderer.save_to_png(str(png_path), dpi=72)  # Lower DPI for testing
    assert success, "PNG export should succeed"

    # Check file exists with reasonable size
    assert png_path.exists(), "PNG file should exist"
    file_size = png_path.stat().st_size
    assert file_size > 100, "PNG file should have reasonable size"


def test_empty_strip(temp_output_dir):
    """Test renderer with empty strip."""
    empty_strip = LabelStrip()
    renderer = StripRenderer(empty_strip)

    # Test dimensions
    _width_px, _height_px = renderer.get_strip_dimensions_px()
    width_mm, height_mm = renderer.get_strip_dimensions_mm()
    assert width_mm >= 0
    assert height_mm > 0

    # Test PNG export (should handle gracefully)
    png_path = temp_output_dir / "test_empty_strip.png"
    success = renderer.save_to_png(str(png_path), dpi=72)
    assert success or not empty_strip.get_total_width(), "Empty strip export handled gracefully"


def test_high_dpi_export(temp_output_dir):
    """Test high DPI PNG export."""
    # Create a simple strip
    strip = LabelStrip()
    strip.set_content_segment_count(1)
    strip.content_cell_width = 20.0

    # Update the segment
    segments = strip.content_segments
    if segments:
        segments[0].text = "TEST"
        segments[0].background_color = Color(100, 150, 200)
        segments[0].text_color = Color(255, 255, 255)

    renderer = StripRenderer(strip)

    # Test different DPI values
    dpi_values = [72, 150]  # Reduced for faster tests
    for dpi in dpi_values:
        png_path = temp_output_dir / f"test_strip_{dpi}dpi.png"
        success = renderer.save_to_png(str(png_path), dpi=dpi)
        assert success, f"Export at {dpi} DPI should succeed"
        assert png_path.exists(), f"PNG file at {dpi} DPI should exist"
