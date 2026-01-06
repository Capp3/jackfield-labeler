#!/usr/bin/env python
"""
Jackfield Labeler - A utility to create strip labels for jackfields.
"""

import sys
from pathlib import Path

from PyQt6.QtCore import QSettings, QStandardPaths
from PyQt6.QtWidgets import QApplication

from jackfield_labeler.utils.logger import configure_logging, get_logger
from jackfield_labeler.views.main_window import MainWindow


def main(args: list[str] | None = None) -> int:
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
    app.setOrganizationName("capp3")

    # Load logging settings from QSettings
    settings = QSettings()
    log_level = settings.value("logging/level", "INFO", type=str)
    log_to_file = settings.value("logging/file_enabled", False, type=bool)

    # Determine log file path
    if log_to_file:
        app_data_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        log_file_path = str(Path(app_data_dir) / "logs" / "jackfield_labeler.log")
    else:
        log_file_path = None

    # Initialize logging system
    configure_logging(level=log_level, log_to_file=log_to_file, log_file_path=log_file_path)

    # Get logger for this module
    logger = get_logger(__name__)
    logger.info("Jackfield Labeler application starting")
    logger.debug(f"Log level: {log_level}, File logging: {log_to_file}")

    # Create and show main window
    window = MainWindow()
    window.show()

    logger.info("Main window displayed")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
