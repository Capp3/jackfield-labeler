"""
Project management utilities for saving and loading label strip projects.
"""

import json
import os
from typing import Any

from jackfield_labeler.models.label_strip import LabelStrip


class ProjectManager:
    """Manages saving and loading of label strip projects."""

    PROJECT_EXTENSION = ".jlp"  # Jackfield Labeler Project
    PROJECT_FILTER = "Jackfield Labeler Projects (*.jlp);;All Files (*)"

    @staticmethod
    def save_project(label_strip: LabelStrip, file_path: str) -> bool:
        """
        Save a label strip project to a file.

        Args:
            label_strip: The label strip to save
            file_path: Path where the project should be saved

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Ensure the file has the correct extension
            if not file_path.lower().endswith(ProjectManager.PROJECT_EXTENSION):
                file_path += ProjectManager.PROJECT_EXTENSION

            # Create the project data structure
            project_data = {
                "version": "1.0",
                "application": "Jackfield Labeler",
                "label_strip": label_strip.to_dict(),
                "metadata": {"created_by": "Jackfield Labeler", "file_format_version": "1.0"},
            }

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write the project file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Error saving project: {e}")
            return False

    @staticmethod
    def load_project(file_path: str) -> LabelStrip | None:
        """
        Load a label strip project from a file.

        Args:
            file_path: Path to the project file

        Returns:
            The loaded LabelStrip instance, or None if loading failed
        """
        try:
            if not os.path.exists(file_path):
                print(f"Project file not found: {file_path}")
                return None

            with open(file_path, encoding="utf-8") as f:
                project_data = json.load(f)

            # Validate project file format
            if not ProjectManager._validate_project_data(project_data):
                print("Invalid project file format")
                return None

            # Extract the label strip data
            label_strip_data = project_data.get("label_strip", {})

            # Create and return the label strip
            return LabelStrip.from_dict(label_strip_data)

        except json.JSONDecodeError as e:
            print(f"Error parsing project file: {e}")
            return None
        except Exception as e:
            print(f"Error loading project: {e}")
            return None

    @staticmethod
    def _validate_project_data(data: dict[str, Any]) -> bool:
        """
        Validate the structure of project data.

        Args:
            data: Project data dictionary

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["version", "application", "label_strip"]

        for field in required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return False

        # Check if it's a Jackfield Labeler project
        if data.get("application") != "Jackfield Labeler":
            print(f"Not a Jackfield Labeler project: {data.get('application')}")
            return False

        # Check version compatibility (for future use)
        version = data.get("version", "")
        if not version.startswith("1."):
            print(f"Unsupported project version: {version}")
            return False

        return True

    @staticmethod
    def get_project_info(file_path: str) -> dict[str, Any] | None:
        """
        Get basic information about a project file without fully loading it.

        Args:
            file_path: Path to the project file

        Returns:
            Dictionary with project info, or None if file can't be read
        """
        try:
            if not os.path.exists(file_path):
                return None

            with open(file_path, encoding="utf-8") as f:
                project_data = json.load(f)

            # Extract basic info
            info = {
                "version": project_data.get("version", "Unknown"),
                "application": project_data.get("application", "Unknown"),
                "file_size": os.path.getsize(file_path),
                "modified_time": os.path.getmtime(file_path),
            }

            # Try to get some label strip info
            label_strip_data = project_data.get("label_strip", {})
            if label_strip_data:
                info.update({
                    "strip_height": label_strip_data.get("height", 0),
                    "content_cell_width": label_strip_data.get("content_cell_width", 0),
                    "segment_count": len(label_strip_data.get("segments", [])),
                })

            return info
        except Exception as e:
            print(f"Error reading project info: {e}")
            return None

    @staticmethod
    def is_valid_project_file(file_path: str) -> bool:
        """
        Check if a file is a valid Jackfield Labeler project.

        Args:
            file_path: Path to check

        Returns:
            True if valid project file, False otherwise
        """
        try:
            if not file_path.lower().endswith(ProjectManager.PROJECT_EXTENSION):
                return False

            info = ProjectManager.get_project_info(file_path)
            return info is not None and info.get("application") == "Jackfield Labeler"

        except Exception:
            return False
