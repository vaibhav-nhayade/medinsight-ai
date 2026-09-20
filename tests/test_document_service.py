from pathlib import Path

from backend.models.document import DocumentRecord
from backend.repositories.document_repository import DocumentRepository
from backend.services.document_service import DocumentService


def create_service():
    """
    Create an isolated document service for testing.
    """

    service = DocumentService()

    # Replace the shared repository with an isolated test repository.
    import backend.services.document_service as module

    module.document_repository = DocumentRepository()

    return service


def create_document() -> DocumentRecord:
    return DocumentRecord(
        document_id="test-document-001",
        original_filename="medical_report.pdf",
        file_type="pdf",
        size_bytes=2048,
        storage_path=Path(
            "data/uploads/test-document.pdf"
        ),
    )


def test_register_document():
    service = create_service()

    document = create_document()

    result = service.register(document)

    assert result.document_id == "test-document-001"
    assert result.status == "uploaded"


def test_document_processing_status():
    service = create_service()

    document = create_document()
    service.register(document)

    service.mark_processing(
        "test-document-001"
    )

    result = service.get(
        "test-document-001"
    )

    assert result is not None
    assert result.status == "processing"


def test_document_processed_status():
    service = create_service()

    document = create_document()
    service.register(document)

    service.mark_processed(
        "test-document-001"
    )

    result = service.get(
        "test-document-001"
    )

    assert result is not None
    assert result.status == "processed"


def test_document_failed_status():
    service = create_service()

    document = create_document()
    service.register(document)

    service.mark_failed(
        "test-document-001"
    )

    result = service.get(
        "test-document-001"
    )

    assert result is not None
    assert result.status == "failed"