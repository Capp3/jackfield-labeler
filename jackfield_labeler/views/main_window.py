"""
Main application window for the Jackfield Labeler.
"""

import os

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from jackfield_labeler import __version__
from jackfield_labeler.views.designer_tab import DesignerTab
from jackfield_labeler.views.preview_tab import PreviewTab
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
        self.preview_tab = PreviewTab()
        self.settings_tab = SettingsTab()

        # Connect settings to designer tab
        self.settings_tab.settings_changed.connect(self._on_settings_changed)

        # Connect designer changes to preview
        self.designer_tab.control_panel.strip_changed.connect(self._update_preview)
        self.designer_tab.segment_table.segment_changed.connect(self._update_preview)

        # Add tabs to tab widget
        self.tab_widget.addTab(self.designer_tab, "Designer")
        self.tab_widget.addTab(self.preview_tab, "Preview")
        self.tab_widget.addTab(self.settings_tab, "Settings")

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Create menu bar
        self.create_menus()

        # Initialize project state
        self._current_project_path = None
        self._project_modified = False

        # Connect signals to track modifications
        self.designer_tab.control_panel.strip_changed.connect(self._mark_project_modified)
        self.designer_tab.segment_table.segment_changed.connect(self._mark_project_modified)
        self.settings_tab.settings_changed.connect(self._mark_project_modified)

        # Update window title
        self._update_window_title()

    def _on_settings_changed(self):
        """Handle settings changes from the settings tab."""
        # Update the designer tab's strip settings
        self.designer_tab.strip.settings = self.settings_tab.settings
        self.status_bar.showMessage("Settings updated", 2000)
        # Update preview
        self._update_preview()

    def _update_preview(self):
        """Update the preview tab with the current strip."""
        self.preview_tab.update_preview(self.designer_tab.strip)

    def create_menus(self):
        """Create application menus."""
        # File menu
        file_menu = self.menuBar().addMenu("&File")

        # New action
        new_action = file_menu.addAction("&New")
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)

        # Open action
        open_action = file_menu.addAction("&Open...")
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_project)

        # Save action
        save_action = file_menu.addAction("&Save")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_project)

        # Save As action
        save_as_action = file_menu.addAction("Save &As...")
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_project_as)

        file_menu.addSeparator()

        # Generate PDF action
        generate_pdf_action = file_menu.addAction("&Generate PDF...")
        generate_pdf_action.setShortcut("Ctrl+P")
        generate_pdf_action.triggered.connect(self.generate_pdf)

        # Export PNG action
        export_png_action = file_menu.addAction("Export &PNG...")
        export_png_action.setShortcut("Ctrl+E")
        export_png_action.triggered.connect(self.export_png)

        file_menu.addSeparator()

        # Exit action
        exit_action = file_menu.addAction("E&xit")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        # Help menu
        help_menu = self.menuBar().addMenu("&Help")

        # User Guide action
        user_guide_action = help_menu.addAction("User &Guide")
        user_guide_action.setShortcut("F1")
        user_guide_action.triggered.connect(self.show_user_guide)

        # Keyboard Shortcuts action
        shortcuts_action = help_menu.addAction("&Keyboard Shortcuts")
        shortcuts_action.setShortcut("Ctrl+K")
        shortcuts_action.triggered.connect(self.show_keyboard_shortcuts)

        # Technical Documentation action
        technical_action = help_menu.addAction("&Technical Documentation")
        technical_action.setShortcut("Ctrl+T")
        technical_action.triggered.connect(self.show_technical_docs)

        help_menu.addSeparator()

        # About action
        about_action = help_menu.addAction("&About")
        about_action.triggered.connect(self.show_about)

    def new_project(self):
        """Create a new label strip project."""
        from PyQt6.QtWidgets import QMessageBox

        # Check if current project has unsaved changes
        if self._has_unsaved_changes():
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before creating a new project?",
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
            )

            if reply == QMessageBox.StandardButton.Save:
                if not self.save_project():
                    return  # Save was cancelled or failed
            elif reply == QMessageBox.StandardButton.Cancel:
                return  # User cancelled

        # Reset the designer tab to create a new project
        self.designer_tab.reset_ui()
        self.settings_tab.reset_ui()
        self._current_project_path = None
        self._project_modified = False
        self._update_window_title()
        self.status_bar.showMessage("New project created", 3000)

    def open_project(self):
        """Open an existing label strip project."""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        from jackfield_labeler.utils import ProjectManager

        # Check if current project has unsaved changes
        if self._has_unsaved_changes():
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before opening another project?",
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
            )

            if reply == QMessageBox.StandardButton.Save:
                if not self.save_project():
                    return  # Save was cancelled or failed
            elif reply == QMessageBox.StandardButton.Cancel:
                return  # User cancelled

        # Get file path to open
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", ProjectManager.get_last_directory(), ProjectManager.PROJECT_FILTER
        )

        if not file_path:
            return  # User cancelled

        # Load the project
        try:
            label_strip = ProjectManager.load_project(file_path)
            if label_strip is None:
                QMessageBox.critical(
                    self,
                    "Load Error",
                    f"Failed to load project from:\n{file_path}\n\nThe file may be corrupted or in an unsupported format.",
                )
                return

            # Update the UI with the loaded project
            self.designer_tab.load_label_strip(label_strip)
            self.settings_tab.settings = label_strip.settings
            self.settings_tab.reset_ui()

            # Update project state
            self._current_project_path = file_path
            self._project_modified = False
            self._update_window_title()

            self.status_bar.showMessage(f"Project opened: {file_path}", 5000)

        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"An unexpected error occurred while loading the project:\n{e!s}")

    def save_project(self) -> bool:
        """Save the current label strip project."""
        if self._current_project_path is None:
            return self.save_project_as()
        else:
            return self._save_to_path(self._current_project_path)

    def save_project_as(self) -> bool:
        """Save the current label strip project with a new name."""
        from PyQt6.QtWidgets import QFileDialog

        from jackfield_labeler.utils import ProjectManager

        # Get file path to save to
        default_path = os.path.join(ProjectManager.get_last_directory(), "untitled.jlp")
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Project As", default_path, ProjectManager.PROJECT_FILTER)

        if not file_path:
            return False  # User cancelled

        # Save to the new path
        if self._save_to_path(file_path):
            self._current_project_path = file_path
            self._update_window_title()
            return True
        else:
            return False

    def generate_pdf(self):
        """Generate a PDF from the current label strip design."""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        from jackfield_labeler.utils import PDFGenerator, ProjectManager

        # Get the current label strip from the designer tab
        label_strip = self.designer_tab.strip

        # Check if there are any segments to generate
        if label_strip.get_total_width() == 0:
            QMessageBox.warning(
                self, "No Content", "Please add some segments to the label strip before generating a PDF."
            )
            return

        # Get output file path
        default_path = os.path.join(ProjectManager.get_last_directory(), "label_strip.pdf")
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", default_path, "PDF Files (*.pdf);;All Files (*)")

        if not file_path:
            return  # User cancelled

        try:
            # Create PDF generator
            pdf_generator = PDFGenerator(label_strip)

            # Generate the PDF using rotation from settings
            success = pdf_generator.generate_pdf(file_path)

            if success:
                self.status_bar.showMessage(f"PDF generated successfully: {file_path}", 5000)
                QMessageBox.information(self, "PDF Generated", f"PDF has been saved to:\n{file_path}")
            else:
                self.status_bar.showMessage("Failed to generate PDF", 3000)
                QMessageBox.critical(
                    self,
                    "PDF Generation Failed",
                    "An error occurred while generating the PDF. Please check your label strip configuration.",
                )

        except Exception as e:
            self.status_bar.showMessage("Error generating PDF", 3000)
            QMessageBox.critical(self, "PDF Generation Error", f"An unexpected error occurred:\n{e!s}")

    def export_png(self):
        """Export the current label strip design as a PNG file."""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        from jackfield_labeler.utils import ProjectManager, StripRenderer

        # Get the current label strip from the designer tab
        label_strip = self.designer_tab.strip

        # Check if there are any segments to export
        if label_strip.get_total_width() == 0:
            QMessageBox.warning(
                self, "No Content", "Please add some segments to the label strip before exporting a PNG."
            )
            return

        # Get output file path
        default_path = os.path.join(ProjectManager.get_last_directory(), "label_strip.png")
        file_path, _ = QFileDialog.getSaveFileName(self, "Export PNG", default_path, "PNG Files (*.png);;All Files (*)")

        if not file_path:
            return  # User cancelled

        try:
            # Create strip renderer
            renderer = StripRenderer(label_strip)

            # Export PNG at 300 DPI (no rotation - sized to strip)
            success = renderer.save_to_png(file_path, dpi=300)

            if success:
                self.status_bar.showMessage(f"PNG exported successfully: {file_path}", 5000)
                QMessageBox.information(self, "PNG Exported", f"PNG has been saved to:\n{file_path}")
            else:
                self.status_bar.showMessage("Failed to export PNG", 3000)
                QMessageBox.critical(
                    self,
                    "PNG Export Failed",
                    "An error occurred while exporting the PNG. Please check your label strip configuration.",
                )

        except Exception as e:
            self.status_bar.showMessage("Error exporting PNG", 3000)
            QMessageBox.critical(self, "PNG Export Error", f"An unexpected error occurred:\n{e!s}")

    def show_user_guide(self):
        """Show the user guide."""
        self._show_documentation("User Guide", "docs/user-guide.md")

    def show_keyboard_shortcuts(self):
        """Show keyboard shortcuts."""
        shortcuts_html = """
        <h2>Keyboard Shortcuts</h2>
        <table border="1" cellspacing="0" cellpadding="3">
            <tr><th>Shortcut</th><th>Action</th></tr>
            <tr><td>Ctrl+N</td><td>New Project</td></tr>
            <tr><td>Ctrl+O</td><td>Open Project</td></tr>
            <tr><td>Ctrl+S</td><td>Save Project</td></tr>
            <tr><td>Ctrl+Shift+S</td><td>Save Project As</td></tr>
            <tr><td>Ctrl+P</td><td>Generate PDF</td></tr>
            <tr><td>Ctrl+E</td><td>Export PNG</td></tr>
            <tr><td>Ctrl+Q</td><td>Exit</td></tr>
            <tr><td>F1</td><td>Show Help</td></tr>
        </table>
        """
        self._show_html_documentation("Keyboard Shortcuts", shortcuts_html)

    def show_technical_docs(self):
        """Show technical documentation."""
        self._show_documentation("Technical Documentation", "docs/technical.md")

    def _show_documentation(self, title: str, md_file_path: str):
        """
        Show documentation from a markdown file.

        Args:
            title: The title for the dialog window
            md_file_path: Path to the markdown file
        """
        try:
            # Get the absolute path to the documentation file
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            file_path = os.path.join(base_dir, md_file_path)

            # Check if file exists
            if not os.path.exists(file_path):
                QMessageBox.warning(
                    self, "Documentation Not Found", f"The documentation file '{md_file_path}' could not be found."
                )
                return

            # Read the markdown file
            with open(file_path, encoding="utf-8") as f:
                markdown_content = f.read()

            # Convert markdown to HTML (basic conversion)
            try:
                import markdown

                html_content = markdown.markdown(markdown_content, extensions=["tables", "fenced_code"])
            except ImportError:
                # Basic fallback if markdown module is not available
                html_content = f"<pre>{markdown_content}</pre>"

            # Show the documentation in a dialog
            self._show_html_documentation(title, html_content)

        except Exception as e:
            QMessageBox.critical(
                self, "Documentation Error", f"An error occurred while loading the documentation:\n{e!s}"
            )

    def _show_html_documentation(self, title: str, html_content: str):
        """
        Show HTML content in a dialog window.

        Args:
            title: The title for the dialog window
            html_content: HTML content to display
        """
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(700, 500)

        # Create layout
        layout = QVBoxLayout(dialog)

        # Create text browser
        text_browser = QTextBrowser(dialog)
        text_browser.setHtml(html_content)
        text_browser.setOpenExternalLinks(True)

        # Set font
        font = QFont("Arial", 10)
        text_browser.setFont(font)

        # Add to layout
        layout.addWidget(text_browser)

        # Add buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        # Show dialog
        dialog.exec()

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

    def _mark_project_modified(self):
        """Mark the project as modified."""
        if not self._project_modified:
            self._project_modified = True
            self._update_window_title()

    def _has_unsaved_changes(self) -> bool:
        """Check if the project has unsaved changes."""
        return self._project_modified

    def _update_window_title(self):
        """Update the window title to reflect the current project state."""
        title = f"Jackfield Labeler v{__version__}"

        if self._current_project_path:
            filename = os.path.basename(self._current_project_path)
            title += f" - {filename}"
        else:
            title += " - Untitled"

        if self._project_modified:
            title += " *"

        self.setWindowTitle(title)

    def _save_to_path(self, file_path: str) -> bool:
        """Save the current project to the specified path."""
        from PyQt6.QtWidgets import QMessageBox

        from jackfield_labeler.utils import ProjectManager

        try:
            # Get the current label strip from the designer tab
            label_strip = self.designer_tab.strip

            # Save the project
            success = ProjectManager.save_project(label_strip, file_path)

            if success:
                self._project_modified = False
                self._update_window_title()
                self.status_bar.showMessage(f"Project saved: {file_path}", 5000)
                ProjectManager.set_last_directory(file_path)  # Update last directory
                return True
            else:
                QMessageBox.critical(self, "Save Error", f"Failed to save project to:\n{file_path}")
                return False

        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"An unexpected error occurred while saving the project:\n{e!s}")
            return False
