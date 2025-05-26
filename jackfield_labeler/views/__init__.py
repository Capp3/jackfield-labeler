"""
Views package for the jackfield labeler application.
Contains UI components built with PyQt6.
"""

from jackfield_labeler.views.designer_tab import DesignerTab, SegmentTable, StripControlPanel
from jackfield_labeler.views.main_window import MainWindow
from jackfield_labeler.views.preview_tab import PreviewTab
from jackfield_labeler.views.settings_tab import ColorButton, DefaultFormattingGroup, PageMarginsGroup, SettingsTab

__all__ = [
    # Settings tab
    "ColorButton",
    "DefaultFormattingGroup",
    # Designer tab
    "DesignerTab",
    # Main window
    "MainWindow",
    "PageMarginsGroup",
    # Preview tab
    "PreviewTab",
    "SegmentTable",
    # Settings tab
    "SettingsTab",
    "StripControlPanel",
]
