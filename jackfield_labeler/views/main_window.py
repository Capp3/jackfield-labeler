"""
Main application window for the Jackfield Labeler.
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from jackfield_labeler import __version__
from jackfield_labeler.views.designer_tab import DesignerTab
from jackfield_labeler.views.settings_tab import SettingsTab


class MainWindow(QMainWindow):
    """Main application window containing the designer and settings tabs."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        self.setWindowTitle(f"Jackfield Labeler v{__version__}")
        self.setMinimumSize(800, 600)

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Create tabs
        self.designer_tab = DesignerTab()
        self.settings_tab = SettingsTab()

        # Add tabs to tab widget
        self.tab_widget.addTab(self.designer_tab, "Designer")
        self.tab_widget.addTab(self.settings_tab, "Settings")

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Create menu bar
        self.create_menus()

    def create_menus(self):
        """Create application menus."""
        # File menu
        file_menu = self.menuBar().addMenu("&File")

        # New action
        new_action = file_menu.addAction("&New")
        new_action.triggered.connect(self.new_project)

        # Open action
        open_action = file_menu.addAction("&Open...")
        open_action.triggered.connect(self.open_project)

        # Save action
        save_action = file_menu.addAction("&Save")
        save_action.triggered.connect(self.save_project)

        # Save As action
        save_as_action = file_menu.addAction("Save &As...")
        save_as_action.triggered.connect(self.save_project_as)

        file_menu.addSeparator()

        # Generate PDF action
        generate_pdf_action = file_menu.addAction("&Generate PDF...")
        generate_pdf_action.triggered.connect(self.generate_pdf)

        file_menu.addSeparator()

        # Exit action
        exit_action = file_menu.addAction("E&xit")
        exit_action.triggered.connect(self.close)

        # Help menu
        help_menu = self.menuBar().addMenu("&Help")

        # About action
        about_action = help_menu.addAction("&About")
        about_action.triggered.connect(self.show_about)

    def new_project(self):
        """Create a new label strip project."""
        # To be implemented
        self.status_bar.showMessage("New project created", 3000)

    def open_project(self):
        """Open an existing label strip project."""
        # To be implemented
        self.status_bar.showMessage("Project opened", 3000)

    def save_project(self):
        """Save the current label strip project."""
        # To be implemented
        self.status_bar.showMessage("Project saved", 3000)

    def save_project_as(self):
        """Save the current label strip project with a new name."""
        # To be implemented
        self.status_bar.showMessage("Project saved as new file", 3000)

    def generate_pdf(self):
        """Generate a PDF from the current label strip design."""
        # To be implemented
        self.status_bar.showMessage("PDF generated", 3000)

    def show_about(self):
        """Show the about dialog."""
        QMessageBox.about(
            self,
            "About Jackfield Labeler",
            f"""<h2>Jackfield Labeler v{__version__}</h2>
            <p>A utility to create strip labels for jackfields.</p>
            <p>© 2023 Dom Capparelli</p>
            <p><a href="https://github.com/capp3/jackfield-labeler">https://github.com/capp3/jackfield-labeler</a></p>""",
        )
