"""
Persistent document repository backed by SQLite.
"""

from datetime import datetime, timezone
from pathlib import Path

from backend.database.connection import (
    get_connection,
    initialize_database,
)
from backend.models.document import DocumentRecord


class DocumentRepository:
    """Store and retrieve document metadata using SQLite."""

    def __init__(self) -> None:
        initialize_database()

    def create(
        self,
        document: DocumentRecord,
    ) -> DocumentRecord:
        """Persist a new document."""

        if document.created_at is None:
            document.created_at = datetime.now(
                timezone.utc
            )

        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO documents (
                    document_id,
                    original_filename,
                    file_type,
                    size_bytes,
                    storage_path,
                    status,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    document.document_id,
                    document.original_filename,
                    document.file_type,
                    document.size_bytes,
                    str(document.storage_path),
                    document.status,
                    document.created_at.isoformat(),
                ),
            )

            connection.commit()

        except Exception as exc:
            connection.rollback()

            if "UNIQUE constraint failed" in str(exc):
                raise ValueError(
                    f"Document already exists: "
                    f"{document.document_id}"
                ) from exc

            raise

        finally:
            connection.close()

        return document

    def get(
        self,
        document_id: str,
    ) -> DocumentRecord | None:
        """Retrieve a document by ID."""

        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    document_id,
                    original_filename,
                    file_type,
                    size_bytes,
                    storage_path,
                    status,
                    created_at
                FROM documents
                WHERE document_id = ?
                """,
                (document_id,),
            ).fetchone()

        finally:
            connection.close()

        if row is None:
            return None

        return self._row_to_document(row)

    def update_status(
        self,
        document_id: str,
        status: str,
    ) -> DocumentRecord:
        """Update document processing status."""

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE documents
                SET status = ?
                WHERE document_id = ?
                """,
                (
                    status,
                    document_id,
                ),
            )

            connection.commit()

        finally:
            connection.close()

        if cursor.rowcount == 0:
            raise KeyError(
                f"Document not found: {document_id}"
            )

        document = self.get(document_id)

        if document is None:
            raise KeyError(
                f"Document not found: {document_id}"
            )

        return document

    def list_all(self) -> list[DocumentRecord]:
        """Return all stored documents."""

        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    document_id,
                    original_filename,
                    file_type,
                    size_bytes,
                    storage_path,
                    status,
                    created_at
                FROM documents
                ORDER BY created_at DESC
                """
            ).fetchall()

        finally:
            connection.close()

        return [
            self._row_to_document(row)
            for row in rows
        ]

    @staticmethod
    def _row_to_document(row) -> DocumentRecord:
        """Convert a database row into a domain model."""

        return DocumentRecord(
            document_id=row["document_id"],
            original_filename=row["original_filename"],
            file_type=row["file_type"],
            size_bytes=row["size_bytes"],
            storage_path=Path(row["storage_path"]),
            status=row["status"],
            created_at=datetime.fromisoformat(
                row["created_at"]
            ),
        )


document_repository = DocumentRepository()