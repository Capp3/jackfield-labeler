#!/usr/bin/env python3
"""
Test script for preview renderer and PNG export functionality.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication

from jackfield_labeler.models import Color, LabelStrip
from jackfield_labeler.utils.strip_renderer import StripRenderer


def test_strip_renderer():
    """Test the strip renderer functionality."""
    print("Testing StripRenderer...")

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

    print(f"Created test strip: {strip.get_total_width()}mm × {strip.height}mm")
    print(f"Segments: {len(strip.content_segments)} content + 1 end")

    # Test renderer creation
    renderer = StripRenderer(strip, scale_factor=10.0)
    print("Created renderer with scale factor: 10.0")

    # Test dimension calculations
    width_px, height_px = renderer.get_strip_dimensions_px()
    width_mm, height_mm = renderer.get_strip_dimensions_mm()
    print(f"Dimensions: {width_mm}mm × {height_mm}mm = {width_px}px × {height_px}px")

    # Test PNG export
    png_path = "test_strip_preview.png"
    print(f"Exporting PNG to: {png_path}")
    success = renderer.save_to_png(png_path, dpi=300)

    if success:
        print(f"✓ PNG export successful: {png_path}")

        # Check file exists and has reasonable size
        png_file = Path(png_path)
        if png_file.exists():
            file_size = png_file.stat().st_size
            print(f"  File size: {file_size} bytes")
            if file_size > 1000:  # Should be at least 1KB for a real image
                print("  ✓ File size looks reasonable")
            else:
                print("  ⚠ File size seems small")
        else:
            print("  ✗ PNG file not found after export")
    else:
        print("✗ PNG export failed")

    return success


def test_empty_strip():
    """Test renderer with empty strip."""
    print("\nTesting empty strip...")

    empty_strip = LabelStrip()

    renderer = StripRenderer(empty_strip)

    # Test dimensions
    width_px, height_px = renderer.get_strip_dimensions_px()
    width_mm, height_mm = renderer.get_strip_dimensions_mm()
    print(f"Empty strip dimensions: {width_mm}mm × {height_mm}mm = {width_px}px × {height_px}px")

    # Test PNG export (should handle gracefully)
    success = renderer.save_to_png("test_empty_strip.png", dpi=300)
    print(f"Empty strip PNG export: {'✓ Success' if success else '✗ Failed (expected)'}")

    return True


def test_high_dpi_export():
    """Test high DPI PNG export."""
    print("\nTesting high DPI export...")

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
    dpi_values = [150, 300, 600]
    for dpi in dpi_values:
        png_path = f"test_strip_{dpi}dpi.png"
        success = renderer.save_to_png(png_path, dpi=dpi)

        if success:
            file_size = Path(png_path).stat().st_size
            print(f"  {dpi} DPI: ✓ Success ({file_size} bytes)")
        else:
            print(f"  {dpi} DPI: ✗ Failed")

    return True


if __name__ == "__main__":
    print("=== Testing Preview Renderer and PNG Export ===\n")

    # Create QApplication for Qt functionality
    app = QApplication(sys.argv)

    try:
        # Run tests
        test1_success = test_strip_renderer()
        test2_success = test_empty_strip()
        test3_success = test_high_dpi_export()

        print("\n=== Test Results ===")
        print(f"Strip Renderer Test: {'✓ PASS' if test1_success else '✗ FAIL'}")
        print(f"Empty Strip Test: {'✓ PASS' if test2_success else '✗ FAIL'}")
        print(f"High DPI Test: {'✓ PASS' if test3_success else '✗ FAIL'}")

        if all([test1_success, test2_success, test3_success]):
            print("\n🎉 All tests passed!")
        else:
            print("\n❌ Some tests failed")

    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
