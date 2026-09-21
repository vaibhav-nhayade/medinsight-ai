from datetime import datetime, timezone
from pathlib import Path

from backend.models.document import DocumentRecord
from backend.repositories.document_repository import DocumentRepository


def create_document(
    document_id: str = "persistent-001",
) -> DocumentRecord:
    return DocumentRecord(
        document_id=document_id,
        original_filename="blood_report.pdf",
        file_type="pdf",
        size_bytes=5000,
        storage_path=Path("data/uploads/report.pdf"),
        status="uploaded",
        created_at=datetime.now(timezone.utc),
    )


def test_document_persists_in_database(isolated_database):
    repository = DocumentRepository()

    document = create_document()

    repository.create(document)

    result = repository.get("persistent-001")

    assert result is not None
    assert result.document_id == "persistent-001"
    assert result.original_filename == "blood_report.pdf"


def test_document_status_persists(isolated_database):
    repository = DocumentRepository()

    repository.create(create_document())

    repository.update_status(
        "persistent-001",
        "processing",
    )

    result = repository.get("persistent-001")

    assert result is not None
    assert result.status == "processing"


def test_missing_document_returns_none(isolated_database):
    repository = DocumentRepository()

    result = repository.get("does-not-exist")

    assert result is None