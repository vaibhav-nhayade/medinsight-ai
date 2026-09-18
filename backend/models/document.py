"""
Domain model representing an uploaded medical document.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class DocumentRecord:
    """Metadata associated with an uploaded document."""

    document_id: str
    original_filename: str
    file_type: str
    size_bytes: int
    storage_path: Path
    status: str = "uploaded"
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)