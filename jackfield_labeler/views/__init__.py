"""
Views package for the jackfield labeler application.
Contains UI components built with PyQt6.
"""

from jackfield_labeler.views.designer_tab import DesignerTab, SegmentTable, StripControlPanel, StripPreview
from jackfield_labeler.views.main_window import MainWindow
from jackfield_labeler.views.settings_tab import ColorButton, DefaultFormattingGroup, PageMarginsGroup, SettingsTab

__all__ = [
    # Main window
    "MainWindow",
    # Designer tab
    "DesignerTab",
    "StripControlPanel",
    "SegmentTable",
    "StripPreview",
    # Settings tab
    "SettingsTab",
    "ColorButton",
    "PageMarginsGroup",
    "DefaultFormattingGroup",
]
