"""
Application database initialization.
"""

from backend.database.connection import initialize_database


def initialize_application_database() -> None:
    """Initialize the application database."""

    initialize_database()