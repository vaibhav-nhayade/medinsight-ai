"""
Document repository.

This implementation uses in-memory storage for the MVP.
A database-backed implementation can replace it later.
"""

from backend.models.document import DocumentRecord


class DocumentRepository:
    """Store and retrieve document metadata."""

    def __init__(self) -> None:
        self._documents: dict[str, DocumentRecord] = {}

    def create(
        self,
        document: DocumentRecord,
    ) -> DocumentRecord:
        """Store a new document record."""

        if document.document_id in self._documents:
            raise ValueError(
                f"Document already exists: {document.document_id}"
            )

        self._documents[document.document_id] = document

        return document

    def get(
        self,
        document_id: str,
    ) -> DocumentRecord | None:
        """Return a document by ID."""

        return self._documents.get(document_id)

    def update_status(
        self,
        document_id: str,
        status: str,
    ) -> DocumentRecord:
        """Update document processing status."""

        document = self.get(document_id)

        if document is None:
            raise KeyError(
                f"Document not found: {document_id}"
            )

        document.status = status

        return document

    def list_all(self) -> list[DocumentRecord]:
        """Return all stored documents."""

        return list(self._documents.values())