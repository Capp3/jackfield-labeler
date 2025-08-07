"""
Settings tab for configuring label strip output preferences.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
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

from jackfield_labeler.models import (
    Color,
    PaperSize,
    StripSettings,
)


class ColorButton(QPushButton):
    """Button that shows a color and opens a color picker dialog when clicked."""

    color_changed = pyqtSignal(QColor)

    def __init__(self, color=None, parent=None):
        """Initialize with the given color."""
        super().__init__(parent)
        self._color = color if color is not None else QColor(0, 0, 0)
        self.setFixedSize(24, 24)
        self.clicked.connect(self._on_clicked)
        self._update_stylesheet()

    def _update_stylesheet(self):
        """Update the button stylesheet to show the current color."""
        self.setStyleSheet(f"background-color: {self._color.name()}; border: 1px solid black;")

    def _on_clicked(self):
        """Open a color dialog when the button is clicked."""
        color = QColorDialog.getColor(self._color, self.parent(), "Select Color")
        if color.isValid():
            self._color = color
            self._update_stylesheet()
            self.color_changed.emit(color)

    def color(self):
        """Get the current color."""
        return self._color

    def set_color(self, color):
        """Set the button color."""
        self._color = color
        self._update_stylesheet()


class PageMarginsGroup(QGroupBox):
    """Group box for configuring page margins."""

    margins_changed = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize the page margins group."""
        super().__init__("Page Margins (mm)", parent)
        self.setLayout(QVBoxLayout())

        # Top margin
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Top:"))
        self.top_spinbox = QDoubleSpinBox()
        self.top_spinbox.setRange(0, 50)
        self.top_spinbox.setValue(10.0)
        self.top_spinbox.valueChanged.connect(self._emit_changed)
        top_layout.addWidget(self.top_spinbox)
        self.layout().addLayout(top_layout)

        # Right margin
        right_layout = QHBoxLayout()
        right_layout.addWidget(QLabel("Right:"))
        self.right_spinbox = QDoubleSpinBox()
        self.right_spinbox.setRange(0, 50)
        self.right_spinbox.setValue(10.0)
        self.right_spinbox.valueChanged.connect(self._emit_changed)
        right_layout.addWidget(self.right_spinbox)
        self.layout().addLayout(right_layout)

        # Bottom margin
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(QLabel("Bottom:"))
        self.bottom_spinbox = QDoubleSpinBox()
        self.bottom_spinbox.setRange(0, 50)
        self.bottom_spinbox.setValue(10.0)
        self.bottom_spinbox.valueChanged.connect(self._emit_changed)
        bottom_layout.addWidget(self.bottom_spinbox)
        self.layout().addLayout(bottom_layout)

        # Left margin
        left_layout = QHBoxLayout()
        left_layout.addWidget(QLabel("Left:"))
        self.left_spinbox = QDoubleSpinBox()
        self.left_spinbox.setRange(0, 50)
        self.left_spinbox.setValue(10.0)
        self.left_spinbox.valueChanged.connect(self._emit_changed)
        left_layout.addWidget(self.left_spinbox)
        self.layout().addLayout(left_layout)

    def _emit_changed(self):
        """Emit the margins_changed signal."""
        self.margins_changed.emit()

    def get_margins(self):
        """Get the margin values as a dictionary."""
        return {
            "top": self.top_spinbox.value(),
            "right": self.right_spinbox.value(),
            "bottom": self.bottom_spinbox.value(),
            "left": self.left_spinbox.value(),
        }

    def set_margins(self, margins):
        """Set the margin values from a dictionary."""
        self.top_spinbox.setValue(margins.get("top", 10.0))
        self.right_spinbox.setValue(margins.get("right", 10.0))
        self.bottom_spinbox.setValue(margins.get("bottom", 10.0))
        self.left_spinbox.setValue(margins.get("left", 10.0))


class DefaultFormattingGroup(QGroupBox):
    """Group box for configuring default text formatting."""

    formatting_changed = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize the default formatting group."""
        super().__init__("Default Formatting", parent)
        self.setLayout(QVBoxLayout())

        # Font selection
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font:"))
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont("Arial"))
        self.font_combo.currentFontChanged.connect(self._emit_changed)
        font_layout.addWidget(self.font_combo)
        self.layout().addLayout(font_layout)

        # Font size
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(QLabel("Font Size (pt):"))
        self.font_size_spinbox = QDoubleSpinBox()
        self.font_size_spinbox.setRange(4, 36)
        self.font_size_spinbox.setValue(8.0)
        self.font_size_spinbox.valueChanged.connect(self._emit_changed)
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

    def _emit_changed(self):
        """Emit the formatting_changed signal."""
        self.formatting_changed.emit()

    def get_formatting(self):
        """Get the formatting values as a dictionary."""
        return {
            "font_name": self.font_combo.currentFont().family(),
            "font_size": self.font_size_spinbox.value(),
            "text_color": self.text_color_button.color(),
            "bg_color": self.bg_color_button.color(),
        }

    def set_formatting(self, formatting):
        """Set the formatting values from a dictionary."""
        self.font_combo.setCurrentFont(QFont(formatting.get("font_name", "Arial")))
        self.font_size_spinbox.setValue(formatting.get("font_size", 8.0))
        self.text_color_button.set_color(formatting.get("text_color", QColor(0, 0, 0)))
        self.bg_color_button.set_color(formatting.get("bg_color", QColor(255, 255, 255)))


class RotationGroup(QGroupBox):
    """Group box for configuring PDF rotation."""

    rotation_changed = pyqtSignal()

    def __init__(self, parent=None):
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
        self.rotation_spinbox.valueChanged.connect(self._emit_changed)
        rotation_layout.addWidget(self.rotation_spinbox)
        self.layout().addLayout(rotation_layout)

        # Common rotation buttons
        buttons_layout = QHBoxLayout()

        self.rotate_0_btn = QPushButton("0°")
        self.rotate_0_btn.clicked.connect(lambda: self.set_rotation(0))
        buttons_layout.addWidget(self.rotate_0_btn)

        self.rotate_90_btn = QPushButton("90°")
        self.rotate_90_btn.clicked.connect(lambda: self.set_rotation(90))
        buttons_layout.addWidget(self.rotate_90_btn)

        self.rotate_180_btn = QPushButton("180°")
        self.rotate_180_btn.clicked.connect(lambda: self.set_rotation(180))
        buttons_layout.addWidget(self.rotate_180_btn)

        self.rotate_270_btn = QPushButton("270°")
        self.rotate_270_btn.clicked.connect(lambda: self.set_rotation(270))
        buttons_layout.addWidget(self.rotate_270_btn)

        self.layout().addLayout(buttons_layout)

    def _emit_changed(self):
        """Emit the rotation_changed signal."""
        self.rotation_changed.emit()

    def get_rotation(self):
        """Get the rotation angle."""
        return self.rotation_spinbox.value()

    def set_rotation(self, angle):
        """Set the rotation angle."""
        self.rotation_spinbox.setValue(int(angle))


class SettingsTab(QWidget):
    """Tab for configuring output settings."""

    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
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
        self.paper_size_combo.currentTextChanged.connect(self._on_settings_changed)
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

        # Initialize UI
        self.reset_ui()

    def reset_ui(self):
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

    def _on_settings_changed(self):
        """Handle settings changes."""
        # Apply settings automatically
        self._apply_settings()

    def _apply_settings(self):
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
        self.settings.default_font_name = formatting["font_name"]
        self.settings.default_font_size = formatting["font_size"]

        # Convert QColor to Color
        text_color = formatting["text_color"]
        self.settings.default_text_color = Color(text_color.red(), text_color.green(), text_color.blue())

        bg_color = formatting["bg_color"]
        self.settings.default_background_color = Color(bg_color.red(), bg_color.green(), bg_color.blue())

        # Emit the settings_changed signal
        self.settings_changed.emit()
