#!/usr/bin/env python
"""
Jackfield Labeler - A utility to create strip labels for jackfields.
"""

import sys

from PyQt6.QtWidgets import QApplication

from jackfield_labeler.views.main_window import MainWindow


def main(args: list[str] = None) -> int:
    """
    Main entry point for the application.

    Args:
        args: Command line arguments

    Returns:
        Exit code
    """
    if args is None:
        args = sys.argv

    app = QApplication(args)
    app.setApplicationName("Jackfield Labeler")

    # Create and show main window
    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
