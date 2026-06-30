"""
Shared pytest fixtures for the jackfield-labeler test suite.
"""

import sys

import pytest


@pytest.fixture(scope="session", autouse=True)
def qt_app():
    """
    Ensure a QApplication instance exists for the entire test session.

    Qt operations such as QPixmap require an active QApplication.  Creating it
    at session scope (autouse) means every test module gets it automatically
    without each file having to manage its own instance.
    """
    try:
        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        yield app
    except ImportError:
        # PyQt6 may be unavailable in some lightweight CI configurations.
        yield None
