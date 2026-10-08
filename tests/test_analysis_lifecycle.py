from pathlib import Path

from fastapi.testclient import TestClient

from backend.main import app
from backend.models.document import DocumentRecord
from backend.routes.analysis import report_service
from backend.schemas.report import AnalysisResponse
from backend.services.document_service import document_service


client = TestClient(app)


def create_document(document_id, storage_path):
    return DocumentRecord(
        document_id=document_id,
        original_filename="blood_report.pdf",
        file_type="pdf",
        size_bytes=4096,
        storage_path=Path(storage_path),
    )


def empty_analysis(document_id):
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


def test_analysis_marks_document_processing_before_analysis(
    isolated_database,
    tmp_path,
    monkeypatch,
):
    document_path = tmp_path / "report.pdf"
    document_path.write_bytes(b"test pdf")

    document = create_document(
        "lifecycle-processing",
        document_path,
    )
    document_service.register(document)

    observed_status = []

    def fake_analyze(file_path, document_id):
        current = document_service.get(document_id)
        observed_status.append(current.status)

        return empty_analysis(document_id)

    monkeypatch.setattr(
        report_service,
        "analyze_report",
        fake_analyze,
    )

    response = client.post(
        "/api/v1/reports/lifecycle-processing/analyze"
    )

    assert response.status_code == 200
    assert observed_status == ["processing"]


def test_successful_analysis_ends_with_processed_status(
    isolated_database,
    tmp_path,
    monkeypatch,
):
    document_path = tmp_path / "report.pdf"
    document_path.write_bytes(b"test pdf")

    document = create_document(
        "lifecycle-processed",
        document_path,
    )
    document_service.register(document)

    monkeypatch.setattr(
        report_service,
        "analyze_report",
        lambda file_path, document_id: empty_analysis(
            document_id
        ),
    )

    response = client.post(
        "/api/v1/reports/lifecycle-processed/analyze"
    )

    assert response.status_code == 200

    stored_document = document_service.get(
        "lifecycle-processed"
    )

    assert stored_document.status == "processed"


def test_failed_analysis_ends_with_failed_status(
    isolated_database,
    tmp_path,
    monkeypatch,
):
    document_path = tmp_path / "report.pdf"
    document_path.write_bytes(b"test pdf")

    document = create_document(
        "lifecycle-failed",
        document_path,
    )
    document_service.register(document)

    observed_status = []

    def fake_analyze(file_path, document_id):
        current = document_service.get(document_id)
        observed_status.append(current.status)

        raise ValueError("Invalid report.")

    monkeypatch.setattr(
        report_service,
        "analyze_report",
        fake_analyze,
    )

    response = client.post(
        "/api/v1/reports/lifecycle-failed/analyze"
    )

    assert response.status_code == 400
    assert observed_status == ["processing"]

    stored_document = document_service.get(
        "lifecycle-failed"
    )

    assert stored_document.status == "failed"