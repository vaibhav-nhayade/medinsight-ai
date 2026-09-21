from pathlib import Path

import pytest

from backend.models.document import DocumentRecord
from backend.repositories.document_repository import DocumentRepository


def create_document(document_id: str = "doc-001") -> DocumentRecord:
    return DocumentRecord(
        document_id=document_id,
        original_filename="report.pdf",
        file_type="pdf",
        size_bytes=1024,
        storage_path=Path("data/uploads/report.pdf"),
    )


def test_create_and_get_document(isolated_database):
    repository = DocumentRepository()

    document = create_document()
    repository.create(document)

    result = repository.get("doc-001")

    assert result is not None
    assert result.document_id == "doc-001"
    assert result.original_filename == "report.pdf"


def test_missing_document_returns_none(isolated_database):
    repository = DocumentRepository()

    result = repository.get("does-not-exist")

    assert result is None


def test_duplicate_document_is_rejected(isolated_database):
    repository = DocumentRepository()

    repository.create(create_document())

    with pytest.raises(ValueError):
        repository.create(create_document())


def test_document_status_can_be_updated(isolated_database):
    repository = DocumentRepository()

    repository.create(create_document())

    repository.update_status(
        document_id="doc-001",
        status="processing",
    )

    result = repository.get("doc-001")

    assert result is not None
    assert result.status == "processing"