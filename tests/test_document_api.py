from pathlib import Path

from fastapi.testclient import TestClient

from backend.main import app
from backend.models.document import DocumentRecord
from backend.services.document_service import document_service


client = TestClient(app)


def test_document_not_found():
    response = client.get(
        "/api/v1/documents/non-existent-document"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found."


def test_document_status_endpoint():
    document = DocumentRecord(
        document_id="api-test-document",
        original_filename="blood_report.pdf",
        file_type="pdf",
        size_bytes=4096,
        storage_path=Path(
            "data/uploads/api-test.pdf"
        ),
    )

    document_service.register(document)

    response = client.get(
        "/api/v1/documents/api-test-document"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_id"] == "api-test-document"
    assert data["filename"] == "blood_report.pdf"
    assert data["file_type"] == "pdf"
    assert data["size_bytes"] == 4096
    assert data["status"] == "uploaded"
    assert "created_at" in data