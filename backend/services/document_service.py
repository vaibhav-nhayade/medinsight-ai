"""
Application service for document lifecycle management.
"""

from backend.models.document import DocumentRecord
from backend.repositories.document_repository import (
    document_repository,
)


class DocumentService:
    """Manage document metadata and processing state."""

    def register(
        self,
        document: DocumentRecord,
    ) -> DocumentRecord:
        """Register a newly uploaded document."""

        return document_repository.create(document)

    def get(
        self,
        document_id: str,
    ) -> DocumentRecord | None:
        """Retrieve a document by ID."""

        return document_repository.get(document_id)

    def mark_processing(
        self,
        document_id: str,
    ) -> DocumentRecord:
        """Mark a document as currently being processed."""

        return document_repository.update_status(
            document_id=document_id,
            status="processing",
        )

    def mark_processed(
        self,
        document_id: str,
    ) -> DocumentRecord:
        """Mark a document as successfully processed."""

        return document_repository.update_status(
            document_id=document_id,
            status="processed",
        )

    def mark_failed(
        self,
        document_id: str,
    ) -> DocumentRecord:
        """Mark a document as failed during processing."""

        return document_repository.update_status(
            document_id=document_id,
            status="failed",
        )


document_service = DocumentService()