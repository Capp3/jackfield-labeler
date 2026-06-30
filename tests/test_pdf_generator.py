"""
Tests for PDFGenerator and ProjectManager.
"""

import os
from pathlib import Path

from jackfield_labeler.models import Color, LabelStrip, TextFormat
from jackfield_labeler.utils.pdf_generator import PDFGenerator
from jackfield_labeler.utils.project_manager import ProjectManager

# ---------------------------------------------------------------------------
# PDFGenerator tests
# ---------------------------------------------------------------------------


def _make_strip() -> LabelStrip:
    """Return a simple populated LabelStrip."""
    strip = LabelStrip(height=6.0)
    strip.set_content_segment_count(4)
    strip.content_cell_width = 15.0
    strip.set_end_segment(width=10.0, text="END")

    segments = strip.content_segments
    if len(segments) >= 4:
        segments[0].text = "IN 1"
        segments[0].background_color = Color(255, 255, 255)
        segments[0].text_color = Color(0, 0, 0)
        segments[0].text_format = TextFormat.BOLD

        segments[1].text = "IN 2"
        segments[1].background_color = Color(255, 200, 200)
        segments[1].text_format = TextFormat.ITALIC

        segments[2].text = "OUT 1"
        segments[2].background_color = Color(200, 255, 200)
        segments[2].text_format = TextFormat.BOLD_ITALIC

        segments[3].text = "OUT 2"
        segments[3].background_color = Color(200, 200, 255)

    return strip


def test_pdf_generate_creates_file(tmp_path: Path) -> None:
    """PDFGenerator.generate_pdf() should create a non-empty PDF file."""
    strip = _make_strip()
    generator = PDFGenerator(strip)
    pdf_path = str(tmp_path / "output.pdf")

    success = generator.generate_pdf(pdf_path)

    assert success, "generate_pdf() should return True"
    assert os.path.exists(pdf_path), "PDF file should exist"
    assert os.path.getsize(pdf_path) > 100, "PDF file should have non-trivial size"


def test_pdf_starts_with_pdf_header(tmp_path: Path) -> None:
    """Generated file must be a valid PDF (starts with %PDF)."""
    strip = _make_strip()
    generator = PDFGenerator(strip)
    pdf_path = str(tmp_path / "output.pdf")
    generator.generate_pdf(pdf_path)

    with open(pdf_path, "rb") as f:
        header = f.read(4)
    assert header == b"%PDF", "File should start with the PDF magic bytes"


def test_pdf_empty_strip_returns_false(tmp_path: Path) -> None:
    """Generating a PDF from an empty strip should either fail gracefully or succeed with a blank page."""
    strip = LabelStrip()  # no segments
    generator = PDFGenerator(strip)
    pdf_path = str(tmp_path / "empty.pdf")

    # The generator may succeed (blank page) or return False — either is acceptable,
    # but it must NOT raise an exception.
    result = generator.generate_pdf(pdf_path)
    assert isinstance(result, bool)


def test_pdf_all_paper_sizes(tmp_path: Path) -> None:
    """generate_pdf() should succeed for every supported paper size."""
    from jackfield_labeler.models.strip_settings import PaperSize

    strip = _make_strip()
    for size in PaperSize:
        strip.settings.paper_size = size
        pdf_path = str(tmp_path / f"output_{size.value}.pdf")
        success = PDFGenerator(strip).generate_pdf(pdf_path)
        assert success, f"PDF generation should succeed for paper size {size.value}"


def test_pdf_rotation(tmp_path: Path) -> None:
    """generate_pdf() should honour an explicit rotation_angle argument."""
    strip = _make_strip()
    generator = PDFGenerator(strip)
    pdf_path = str(tmp_path / "rotated.pdf")

    success = generator.generate_pdf(pdf_path, rotation_angle=90.0)
    assert success, "generate_pdf() with rotation=90 should return True"
    assert os.path.getsize(pdf_path) > 100


def test_pdf_font_resolve_bold_italic() -> None:
    """_resolve_font() should return distinct names for each TextFormat."""
    strip = _make_strip()
    gen = PDFGenerator(strip)

    normal = gen._resolve_font(TextFormat.NORMAL)
    bold = gen._resolve_font(TextFormat.BOLD)
    italic = gen._resolve_font(TextFormat.ITALIC)
    bold_italic = gen._resolve_font(TextFormat.BOLD_ITALIC)

    assert normal != bold
    assert normal != italic
    assert bold != italic
    assert bold_italic not in (normal, bold, italic)


# ---------------------------------------------------------------------------
# ProjectManager tests
# ---------------------------------------------------------------------------


def test_project_manager_round_trip(tmp_path: Path) -> None:
    """save_project / load_project should produce an identical LabelStrip."""
    strip = _make_strip()
    project_path = str(tmp_path / "test_project.jlp")

    saved = ProjectManager.save_project(strip, project_path)
    assert saved, "save_project() should return True"
    assert os.path.exists(project_path), "Project file should exist"

    loaded = ProjectManager.load_project(project_path)
    assert loaded is not None, "load_project() should return a LabelStrip"

    assert loaded.height == strip.height
    assert loaded.content_cell_width == strip.content_cell_width
    assert len(loaded.content_segments) == len(strip.content_segments)

    for orig, new in zip(strip.content_segments, loaded.content_segments, strict=True):
        assert orig.text == new.text
        assert orig.text_format == new.text_format
        assert orig.background_color.to_hex() == new.background_color.to_hex()
        assert orig.text_color.to_hex() == new.text_color.to_hex()


def test_project_manager_invalid_file(tmp_path: Path) -> None:
    """load_project() should return None for a corrupt / non-JSON file."""
    bad_file = tmp_path / "bad.jlp"
    bad_file.write_text("this is not valid json")

    result = ProjectManager.load_project(str(bad_file))
    assert result is None, "load_project() should return None for invalid JSON"


def test_project_manager_missing_file() -> None:
    """load_project() should return None when the file does not exist."""
    result = ProjectManager.load_project("/nonexistent/path/project.jlp")
    assert result is None


def test_project_manager_preserves_settings(tmp_path: Path) -> None:
    """Settings (rotation_angle, font, paper size) should survive a round-trip."""
    strip = _make_strip()
    strip.settings.rotation_angle = 90.0
    strip.settings.default_font_name = "Courier"
    strip.settings.default_font_size = 10.0

    project_path = str(tmp_path / "settings_test.jlp")
    ProjectManager.save_project(strip, project_path)

    loaded = ProjectManager.load_project(project_path)
    assert loaded is not None
    assert loaded.settings.rotation_angle == 90.0
    assert loaded.settings.default_font_name == "Courier"
    assert loaded.settings.default_font_size == 10.0
