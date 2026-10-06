from pathlib import Path

from fastapi.testclient import TestClient

from backend.main import app
from backend.models.document import DocumentRecord
from backend.routes.analysis import report_service
from backend.schemas.report import AnalysisResponse
from backend.services.document_service import document_service


client = TestClient(app)


def create_document(
    document_id,
    filename="blood_report.pdf",
    storage_path=None,
):
    return DocumentRecord(
        document_id=document_id,
        original_filename=filename,
        file_type="pdf",
        size_bytes=4096,
        storage_path=Path(storage_path or "data/uploads/report.pdf"),
    )


def make_analysis_response(document_id="test-001"):
    return AnalysisResponse(
        document_id=document_id,
        filename="blood_report.pdf",
        results=[],
        findings=[],
        summary={
            "total_results": 0,
            "normal_results": 0,
            "low_results": 0,
            "high_results": 0,
            "unknown_results": 0,
            "findings_count": 0,
            "verification_required": 0,
        },
    )


def test_analysis_endpoint_success(
    isolated_database,
    tmp_path,
    monkeypatch,
):
    document_path = tmp_path / "blood_report.pdf"
    document_path.write_bytes(b"test pdf")

    document = create_document(
        document_id="analysis-success",
        storage_path=document_path,
    )
    document_service.register(document)

    monkeypatch.setattr(
        report_service,
        "analyze_report",
        lambda file_path, document_id: make_analysis_response(
            document_id
        ),
    )

    response = client.post(
        "/api/v1/reports/analysis-success/analyze"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_id"] == "analysis-success"
    assert data["filename"] == "blood_report.pdf"
    assert data["results"] == []
    assert data["findings"] == []
    assert data["summary"]["total_results"] == 0

    stored_document = document_service.get("analysis-success")

    assert stored_document.status == "processed"


def test_analysis_endpoint_returns_404_for_unknown_document(
    isolated_database,
):
    response = client.post(
        "/api/v1/reports/missing-document/analyze"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found."


def test_analysis_endpoint_returns_400_for_invalid_report(
    isolated_database,
    tmp_path,
    monkeypatch,
):
    document_path = tmp_path / "invalid.pdf"
    document_path.write_bytes(b"invalid")

    document = create_document(
        document_id="analysis-invalid",
        storage_path=document_path,
    )
    document_service.register(document)

    def raise_value_error(file_path, document_id):
        raise ValueError("Invalid medical report.")

    monkeypatch.setattr(
        report_service,
        "analyze_report",
        raise_value_error,
    )

    response = client.post(
        "/api/v1/reports/analysis-invalid/analyze"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid medical report."

    stored_document = document_service.get("analysis-invalid")

    assert stored_document.status == "failed"


def test_analysis_endpoint_returns_404_when_file_is_missing(
    isolated_database,
    monkeypatch,
):
    document = create_document(
        document_id="analysis-missing-file",
        storage_path="data/uploads/missing.pdf",
    )
    document_service.register(document)

    def raise_file_not_found(file_path, document_id):
        raise FileNotFoundError("File not found.")

    monkeypatch.setattr(
        report_service,
        "analyze_report",
        raise_file_not_found,
    )

    response = client.post(
        "/api/v1/reports/analysis-missing-file/analyze"
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "Stored document could not be found."
    )

    stored_document = document_service.get(
        "analysis-missing-file"
    )

    assert stored_document.status == "failed"


def test_analysis_endpoint_returns_500_for_unexpected_error(
    isolated_database,
    tmp_path,
    monkeypatch,
):
    document_path = tmp_path / "error.pdf"
    document_path.write_bytes(b"test pdf")

    document = create_document(
        document_id="analysis-error",
        storage_path=document_path,
    )
    document_service.register(document)

    def raise_unexpected_error(file_path, document_id):
        raise RuntimeError("Unexpected failure.")

    monkeypatch.setattr(
        report_service,
        "analyze_report",
        raise_unexpected_error,
    )

    response = client.post(
        "/api/v1/reports/analysis-error/analyze"
    )

    assert response.status_code == 500
    assert (
        response.json()["detail"]
        == "Document analysis failed."
    )

    stored_document = document_service.get("analysis-error")

    assert stored_document.status == "failed"