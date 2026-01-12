"""
Settings tab for configuring label strip output preferences.
"""

import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from PyQt6.QtCore import QSettings, QStandardPaths, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDoubleSpinBox,
    QFontComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QWidget as QWidgetType
else:
    QWidgetType = QWidget  # Runtime alias for type annotations

from jackfield_labeler.models import Color, PaperSize, StripSettings
from jackfield_labeler.utils.logger import configure_logging, get_logger


class ColorButton(QPushButton):
    """Button that shows a color and opens a color picker dialog when clicked."""

    color_changed = pyqtSignal(QColor)

    def __init__(self, color: QColor | None = None, parent: QWidgetType | None = None) -> None:
        """Initialize with the given color."""
        super().__init__(parent)
        self._color = color if color is not None else QColor(0, 0, 0)
        self.setFixedSize(24, 24)
        self.clicked.connect(self._on_clicked)  # type: ignore[attr-defined]
        self._update_stylesheet()

    def _update_stylesheet(self) -> None:
        """Update the button stylesheet to show the current color."""
        self.setStyleSheet(f"background-color: {self._color.name()}; border: 1px solid black;")

    def _on_clicked(self) -> None:
        """Open a color dialog when the button is clicked."""
        parent_widget = self.parent()
        if isinstance(parent_widget, QWidget):
            color = QColorDialog.getColor(self._color, parent_widget, "Select Color")
        else:
            color = QColorDialog.getColor(self._color, None, "Select Color")
        if color.isValid():
            self._color = color
            self._update_stylesheet()
            self.color_changed.emit(color)

    def color(self) -> QColor:
        """Get the current color."""
        return self._color

    def set_color(self, color: QColor) -> None:
        """Set the button color."""
        self._color = color
        self._update_stylesheet()


class PageMarginsGroup(QGroupBox):
    """Group box for configuring page margins."""

    margins_changed = pyqtSignal()

    def __init__(self, parent: QWidgetType | None = None) -> None:
        """Initialize the page margins group."""
        super().__init__("Page Margins (mm)", parent)
        self.setLayout(QVBoxLayout())

        # Top margin
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Top:"))
        self.top_spinbox = QDoubleSpinBox()
        self.top_spinbox.setRange(0, 50)
        self.top_spinbox.setValue(10.0)
        self.top_spinbox.valueChanged.connect(self._emit_changed)  # type: ignore[attr-defined]
        top_layout.addWidget(self.top_spinbox)
        self.layout().addLayout(top_layout)

        # Right margin
        right_layout = QHBoxLayout()
        right_layout.addWidget(QLabel("Right:"))
        self.right_spinbox = QDoubleSpinBox()
        self.right_spinbox.setRange(0, 50)
        self.right_spinbox.setValue(10.0)
        self.right_spinbox.valueChanged.connect(self._emit_changed)  # type: ignore[attr-defined]
        right_layout.addWidget(self.right_spinbox)
        self.layout().addLayout(right_layout)

        # Bottom margin
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(QLabel("Bottom:"))
        self.bottom_spinbox = QDoubleSpinBox()
        self.bottom_spinbox.setRange(0, 50)
        self.bottom_spinbox.setValue(10.0)
        self.bottom_spinbox.valueChanged.connect(self._emit_changed)  # type: ignore[attr-defined]
        bottom_layout.addWidget(self.bottom_spinbox)
        self.layout().addLayout(bottom_layout)

        # Left margin
        left_layout = QHBoxLayout()
        left_layout.addWidget(QLabel("Left:"))
        self.left_spinbox = QDoubleSpinBox()
        self.left_spinbox.setRange(0, 50)
        self.left_spinbox.setValue(10.0)
        self.left_spinbox.valueChanged.connect(self._emit_changed)  # type: ignore[attr-defined]
        left_layout.addWidget(self.left_spinbox)
        self.layout().addLayout(left_layout)

    def _emit_changed(self) -> None:
        """Emit the margins_changed signal."""
        self.margins_changed.emit()

    def get_margins(self) -> dict[str, float]:
        """Get the margin values as a dictionary."""
        return {
            "top": self.top_spinbox.value(),
            "right": self.right_spinbox.value(),
            "bottom": self.bottom_spinbox.value(),
            "left": self.left_spinbox.value(),
        }

    def set_margins(self, margins: dict[str, float]) -> None:
        """Set the margin values from a dictionary."""
        self.top_spinbox.setValue(margins.get("top", 10.0))
        self.right_spinbox.setValue(margins.get("right", 10.0))
        self.bottom_spinbox.setValue(margins.get("bottom", 10.0))
        self.left_spinbox.setValue(margins.get("left", 10.0))


class DefaultFormattingGroup(QGroupBox):
    """Group box for configuring default text formatting."""

    formatting_changed = pyqtSignal()

    def __init__(self, parent: QWidgetType | None = None) -> None:
        """Initialize the default formatting group."""
        super().__init__("Default Formatting", parent)
        self.setLayout(QVBoxLayout())

        # Font selection
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font:"))
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont("Arial"))
        self.font_combo.currentFontChanged.connect(self._emit_changed)  # type: ignore[attr-defined]
        font_layout.addWidget(self.font_combo)
        self.layout().addLayout(font_layout)

        # Font size
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(QLabel("Font Size (pt):"))
        self.font_size_spinbox = QDoubleSpinBox()
        self.font_size_spinbox.setRange(4, 36)
        self.font_size_spinbox.setValue(8.0)
        self.font_size_spinbox.valueChanged.connect(self._emit_changed)  # type: ignore[attr-defined]
        font_size_layout.addWidget(self.font_size_spinbox)
        self.layout().addLayout(font_size_layout)

        # Text color
        text_color_layout = QHBoxLayout()
        text_color_layout.addWidget(QLabel("Text Color:"))
        self.text_color_button = ColorButton(QColor(0, 0, 0))
        self.text_color_button.color_changed.connect(self._emit_changed)
        text_color_layout.addWidget(self.text_color_button)
        self.layout().addLayout(text_color_layout)

        # Background color
        bg_color_layout = QHBoxLayout()
        bg_color_layout.addWidget(QLabel("Background Color:"))
        self.bg_color_button = ColorButton(QColor(255, 255, 255))
        self.bg_color_button.color_changed.connect(self._emit_changed)
        bg_color_layout.addWidget(self.bg_color_button)
        self.layout().addLayout(bg_color_layout)

    def _emit_changed(self) -> None:
        """Emit the formatting_changed signal."""
        self.formatting_changed.emit()

    def get_formatting(self) -> dict[str, str | float | QColor]:
        """Get the formatting values as a dictionary."""
        return {
            "font_name": self.font_combo.currentFont().family(),
            "font_size": self.font_size_spinbox.value(),
            "text_color": self.text_color_button.color(),
            "bg_color": self.bg_color_button.color(),
        }

    def set_formatting(self, formatting: dict[str, str | float | QColor]) -> None:
        """Set the formatting values from a dictionary."""
        font_name = formatting.get("font_name", "Arial")
        if not isinstance(font_name, str):
            raise TypeError(f"Expected str for font_name, got {type(font_name).__name__}")
        self.font_combo.setCurrentFont(QFont(font_name))
        font_size = formatting.get("font_size", 8.0)
        if not isinstance(font_size, int | float):
            raise TypeError(f"Expected int or float for font_size, got {type(font_size).__name__}")
        self.font_size_spinbox.setValue(float(font_size))
        text_color = formatting.get("text_color", QColor(0, 0, 0))
        if not isinstance(text_color, QColor):
            raise TypeError(f"Expected QColor for text_color, got {type(text_color).__name__}")
        self.text_color_button.set_color(text_color)
        bg_color = formatting.get("bg_color", QColor(255, 255, 255))
        if not isinstance(bg_color, QColor):
            raise TypeError(f"Expected QColor for bg_color, got {type(bg_color).__name__}")
        self.bg_color_button.set_color(bg_color)


class RotationGroup(QGroupBox):
    """Group box for configuring PDF rotation."""

    rotation_changed = pyqtSignal()

    def __init__(self, parent: QWidgetType | None = None) -> None:
        """Initialize the rotation group."""
        super().__init__("PDF Rotation", parent)
        self.setLayout(QVBoxLayout())

        # Rotation angle
        rotation_layout = QHBoxLayout()
        rotation_layout.addWidget(QLabel("Rotation Angle (degrees):"))
        self.rotation_spinbox = QSpinBox()
        self.rotation_spinbox.setRange(-360, 360)
        self.rotation_spinbox.setValue(0)
        self.rotation_spinbox.setSuffix("°")
        self.rotation_spinbox.valueChanged.connect(self._emit_changed)  # type: ignore[attr-defined]
        rotation_layout.addWidget(self.rotation_spinbox)
        self.layout().addLayout(rotation_layout)

        # Common rotation buttons
        buttons_layout = QHBoxLayout()

        self.rotate_0_btn = QPushButton("0°")
        self.rotate_0_btn.clicked.connect(lambda: self.set_rotation(0))  # type: ignore[attr-defined]
        buttons_layout.addWidget(self.rotate_0_btn)

        self.rotate_90_btn = QPushButton("90°")
        self.rotate_90_btn.clicked.connect(lambda: self.set_rotation(90))  # type: ignore[attr-defined]
        buttons_layout.addWidget(self.rotate_90_btn)

        self.rotate_180_btn = QPushButton("180°")
        self.rotate_180_btn.clicked.connect(lambda: self.set_rotation(180))  # type: ignore[attr-defined]
        buttons_layout.addWidget(self.rotate_180_btn)

        self.rotate_270_btn = QPushButton("270°")
        self.rotate_270_btn.clicked.connect(lambda: self.set_rotation(270))  # type: ignore[attr-defined]
        buttons_layout.addWidget(self.rotate_270_btn)

        self.layout().addLayout(buttons_layout)

    def _emit_changed(self) -> None:
        """Emit the rotation_changed signal."""
        self.rotation_changed.emit()

    def get_rotation(self) -> int:
        """Get the rotation angle."""
        return self.rotation_spinbox.value()

    def set_rotation(self, angle: float) -> None:
        """Set the rotation angle."""
        self.rotation_spinbox.setValue(int(angle))


class LoggingGroup(QGroupBox):
    """Group box for configuring application logging."""

    logging_changed = pyqtSignal()

    def __init__(self, parent: QWidgetType | None = None) -> None:
        """Initialize the logging group."""
        super().__init__("Logging", parent)
        self.setLayout(QVBoxLayout())

        # Log level selection
        level_layout = QHBoxLayout()
        level_layout.addWidget(QLabel("Log Level:"))
        self.level_combo = QComboBox()
        self.level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.level_combo.setCurrentText("INFO")
        self.level_combo.currentTextChanged.connect(self._emit_changed)  # type: ignore[attr-defined]
        level_layout.addWidget(self.level_combo)
        self.layout().addLayout(level_layout)

        # File logging checkbox
        file_layout = QHBoxLayout()
        self.file_checkbox = QCheckBox("Save logs to file")
        self.file_checkbox.setChecked(False)
        self.file_checkbox.stateChanged.connect(self._emit_changed)  # type: ignore[attr-defined]
        file_layout.addWidget(self.file_checkbox)
        self.layout().addLayout(file_layout)

        # Open log folder button
        button_layout = QHBoxLayout()
        self.open_logs_button = QPushButton("Open Log Folder")
        self.open_logs_button.clicked.connect(self._open_log_folder)  # type: ignore[attr-defined]
        button_layout.addWidget(self.open_logs_button)
        button_layout.addStretch()
        self.layout().addLayout(button_layout)

    def _emit_changed(self) -> None:
        """Emit the logging_changed signal."""
        self.logging_changed.emit()

    def _open_log_folder(self) -> None:
        """Open the log folder in the system file manager."""
        app_data_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        log_dir = Path(app_data_dir) / "logs"

        # Create directory if it doesn't exist
        log_dir.mkdir(parents=True, exist_ok=True)

        # Open in file manager (cross-platform)
        if sys.platform == "darwin":  # macOS
            subprocess.run(["open", str(log_dir)], check=False)  # noqa: S603, S607
        elif sys.platform == "win32":  # Windows
            subprocess.run(["explorer", str(log_dir)], check=False)  # noqa: S603, S607
        else:  # Linux
            subprocess.run(["xdg-open", str(log_dir)], check=False)  # noqa: S603, S607

    def get_logging_config(self) -> dict[str, str | bool]:
        """Get the logging configuration as a dictionary."""
        return {
            "level": self.level_combo.currentText(),
            "file_enabled": self.file_checkbox.isChecked(),
        }

    def set_logging_config(self, config: dict[str, str | bool]) -> None:
        """Set the logging configuration from a dictionary."""
        # Set log level
        level = config.get("level", "INFO")
        if not isinstance(level, str):
            raise TypeError(f"Expected str for level, got {type(level).__name__}")
        index = self.level_combo.findText(level)
        if index >= 0:
            self.level_combo.setCurrentIndex(index)

        # Set file logging checkbox
        file_enabled = config.get("file_enabled", False)
        if not isinstance(file_enabled, bool):
            raise TypeError(f"Expected bool for file_enabled, got {type(file_enabled).__name__}")
        self.file_checkbox.setChecked(file_enabled)


class SettingsTab(QWidget):
    """Tab for configuring output settings."""

    settings_changed = pyqtSignal()

    def __init__(self, parent: QWidgetType | None = None) -> None:
        """Initialize the settings tab."""
        super().__init__(parent)

        # Create main layout with improved spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(20)

        # Create scroll area for settings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Create scroll content widget
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(8, 8, 8, 8)
        scroll_layout.setSpacing(20)

        # Paper size group
        paper_group = QGroupBox("📄 Paper Settings")
        paper_group.setLayout(QVBoxLayout())
        paper_group.layout().setSpacing(12)
        paper_group.layout().setContentsMargins(16, 20, 16, 16)

        # Paper size selection
        paper_size_layout = QHBoxLayout()
        paper_size_layout.setSpacing(8)
        paper_size_label = QLabel("Paper Size:")
        paper_size_label.setMinimumWidth(120)
        paper_size_layout.addWidget(paper_size_label)

        self.paper_size_combo = QComboBox()
        self.paper_size_combo.addItems([size.value for size in PaperSize])
        self.paper_size_combo.setCurrentText(PaperSize.A3.value)
        self.paper_size_combo.currentTextChanged.connect(self._on_settings_changed)  # type: ignore[attr-defined]
        paper_size_layout.addWidget(self.paper_size_combo)
        paper_size_layout.addStretch()
        paper_group.layout().addLayout(paper_size_layout)

        scroll_layout.addWidget(paper_group)

        # Page margins group
        self.margins_group = PageMarginsGroup()
        scroll_layout.addWidget(self.margins_group)

        # Default formatting group
        self.formatting_group = DefaultFormattingGroup()
        scroll_layout.addWidget(self.formatting_group)

        # Rotation group
        self.rotation_group = RotationGroup()
        scroll_layout.addWidget(self.rotation_group)

        # Logging group
        self.logging_group = LoggingGroup()
        scroll_layout.addWidget(self.logging_group)

        # Add stretch to push all groups to top
        scroll_layout.addStretch()

        # Set scroll area widget
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Initialize settings
        self.settings = StripSettings()

        # Connect signals
        self.margins_group.margins_changed.connect(self._on_settings_changed)
        self.formatting_group.formatting_changed.connect(self._on_settings_changed)
        self.rotation_group.rotation_changed.connect(self._on_settings_changed)
        self.logging_group.logging_changed.connect(self._on_logging_changed)

        # Initialize UI
        self.reset_ui()

    def reset_ui(self) -> None:
        """Reset the UI to match the current settings model."""
        # Reset paper size
        index = self.paper_size_combo.findText(self.settings.paper_size.value)
        if index >= 0:
            self.paper_size_combo.setCurrentIndex(index)

        # Reset margins
        self.margins_group.set_margins({
            "top": self.settings.page_margins.top,
            "right": self.settings.page_margins.right,
            "bottom": self.settings.page_margins.bottom,
            "left": self.settings.page_margins.left,
        })

        # Reset rotation
        self.rotation_group.set_rotation(self.settings.rotation_angle)

        # Reset formatting
        text_color = QColor(*self.settings.default_text_color.to_rgb_tuple())
        bg_color = QColor(*self.settings.default_background_color.to_rgb_tuple())

        self.formatting_group.set_formatting({
            "font_name": self.settings.default_font_name,
            "font_size": self.settings.default_font_size,
            "text_color": text_color,
            "bg_color": bg_color,
        })

    def _on_settings_changed(self) -> None:
        """Handle settings changes."""
        # Apply settings automatically
        self._apply_settings()

    def _on_logging_changed(self) -> None:
        """Handle logging settings changes."""
        logger = get_logger(__name__)

        # Get current logging config
        config = self.logging_group.get_logging_config()

        # Save to QSettings
        settings = QSettings()
        settings.setValue("logging/level", config["level"])
        settings.setValue("logging/file_enabled", config["file_enabled"])

        # Determine log file path
        if config["file_enabled"]:
            app_data_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
            log_file_path = str(Path(app_data_dir) / "logs" / "jackfield_labeler.log")
        else:
            log_file_path = None

        # Reconfigure logging
        level = config["level"]
        if not isinstance(level, str):
            raise TypeError(f"Expected str for level, got {type(level).__name__}")
        file_enabled = config["file_enabled"]
        if not isinstance(file_enabled, bool):
            raise TypeError(f"Expected bool for file_enabled, got {type(file_enabled).__name__}")
        configure_logging(
            level=level,
            log_to_file=file_enabled,
            log_file_path=log_file_path,
        )

        logger.info(
            "Logging configuration updated: level=%s, file=%s",
            config["level"],
            config["file_enabled"],
        )

    def _apply_settings(self) -> None:
        """Apply the current settings to the model."""
        # Update paper size
        self.settings.paper_size = PaperSize(self.paper_size_combo.currentText())

        # Update margins
        margins = self.margins_group.get_margins()
        self.settings.page_margins.top = margins["top"]
        self.settings.page_margins.right = margins["right"]
        self.settings.page_margins.bottom = margins["bottom"]
        self.settings.page_margins.left = margins["left"]

        # Update rotation
        self.settings.rotation_angle = float(self.rotation_group.get_rotation())

        # Update formatting
        formatting = self.formatting_group.get_formatting()
        font_name = formatting["font_name"]
        if not isinstance(font_name, str):
            raise TypeError(f"Expected str for font_name, got {type(font_name).__name__}")
        self.settings.default_font_name = font_name
        font_size = formatting["font_size"]
        if not isinstance(font_size, int | float):
            raise TypeError(f"Expected int or float for font_size, got {type(font_size).__name__}")
        self.settings.default_font_size = float(font_size)

        # Convert QColor to Color
        text_color = formatting["text_color"]
        if not isinstance(text_color, QColor):
            raise TypeError(f"Expected QColor for text_color, got {type(text_color).__name__}")
        self.settings.default_text_color = Color(text_color.red(), text_color.green(), text_color.blue())

        bg_color = formatting["bg_color"]
        if not isinstance(bg_color, QColor):
            raise TypeError(f"Expected QColor for bg_color, got {type(bg_color).__name__}")
        self.settings.default_background_color = Color(bg_color.red(), bg_color.green(), bg_color.blue())

        # Emit the settings_changed signal
        self.settings_changed.emit()
