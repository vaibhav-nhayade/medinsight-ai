"""
API schemas for document metadata and processing status.
"""

from datetime import datetime

from pydantic import BaseModel


class DocumentStatusResponse(BaseModel):
    """Current status and metadata of an uploaded document."""

    document_id: str
    filename: str
    file_type: str
    size_bytes: int
    status: str
    created_at: datetime