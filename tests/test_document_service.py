from pathlib import Path

from backend.models.document import DocumentRecord
from backend.repositories.document_repository import DocumentRepository
from backend.services.document_service import DocumentService


def create_document() -> DocumentRecord:
    return DocumentRecord(
        document_id="test-document-001",
        original_filename="medical_report.pdf",
        file_type="pdf",
        size_bytes=2048,
        storage_path=Path("data/uploads/test-document.pdf"),
    )


def create_service() -> DocumentService:
    return DocumentService()


def test_register_document(isolated_database):
    service = create_service()

    document = create_document()

    result = service.register(document)

    assert result.document_id == "test-document-001"
    assert result.status == "uploaded"


def test_document_processing_status(isolated_database):
    service = create_service()

    service.register(create_document())

    service.mark_processing("test-document-001")

    result = service.get("test-document-001")

    assert result is not None
    assert result.status == "processing"


def test_document_processed_status(isolated_database):
    service = create_service()

    service.register(create_document())

    service.mark_processed("test-document-001")

    result = service.get("test-document-001")

    assert result is not None
    assert result.status == "processed"


def test_document_failed_status(isolated_database):
    service = create_service()

    service.register(create_document())

    service.mark_failed("test-document-001")

    result = service.get("test-document-001")

    assert result is not None
    assert result.status == "failed"