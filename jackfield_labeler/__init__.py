"""Jackfield Labeler - A professional desktop application for creating custom label strips."""

try:
    from importlib import metadata

    __version__ = metadata.version("jackfield-labeler")
except ImportError:
    __version__ = "0.0.0"
