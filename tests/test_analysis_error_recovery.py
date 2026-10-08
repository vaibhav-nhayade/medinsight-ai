from pathlib import Path

from fastapi.testclient import TestClient

from backend.main import app
from backend.models.document import DocumentRecord
from backend.routes.analysis import report_service
from backend.services.document_service import document_service


client = TestClient(app)


def create_document(document_id, storage_path):
    return DocumentRecord(
        document_id=document_id,
        original_filename="report.pdf",
        file_type="pdf",
        size_bytes=1024,
        storage_path=Path(storage_path),
    )


def test_value_error_marks_document_failed(
    isolated_database,
    tmp_path,
    monkeypatch,
):
    path = tmp_path / "report.pdf"
    path.write_bytes(b"test")

    document = create_document(
        "error-recovery-value",
        path,
    )
    document_service.register(document)

    def fail_analysis(file_path, document_id):
        assert document_service.get(document_id).status == "processing"
        raise ValueError("Invalid report.")

    monkeypatch.setattr(
        report_service,
        "analyze_report",
        fail_analysis,
    )

    response = client.post(
        "/api/v1/reports/error-recovery-value/analyze"
    )

    assert response.status_code == 400
    assert document_service.get(
        "error-recovery-value"
    ).status == "failed"


def test_file_not_found_marks_document_failed(
    isolated_database,
    monkeypatch,
):
    document = create_document(
        "error-recovery-file",
        "missing/report.pdf",
    )
    document_service.register(document)

    def fail_analysis(file_path, document_id):
        assert document_service.get(document_id).status == "processing"
        raise FileNotFoundError("Missing file.")

    monkeypatch.setattr(
        report_service,
        "analyze_report",
        fail_analysis,
    )

    response = client.post(
        "/api/v1/reports/error-recovery-file/analyze"
    )

    assert response.status_code == 404
    assert document_service.get(
        "error-recovery-file"
    ).status == "failed"


def test_unexpected_error_marks_document_failed(
    isolated_database,
    tmp_path,
    monkeypatch,
):
    path = tmp_path / "report.pdf"
    path.write_bytes(b"test")

    document = create_document(
        "error-recovery-unexpected",
        path,
    )
    document_service.register(document)

    def fail_analysis(file_path, document_id):
        assert document_service.get(document_id).status == "processing"
        raise RuntimeError("Unexpected error.")

    monkeypatch.setattr(
        report_service,
        "analyze_report",
        fail_analysis,
    )

    response = client.post(
        "/api/v1/reports/error-recovery-unexpected/analyze"
    )

    assert response.status_code == 500
    assert document_service.get(
        "error-recovery-unexpected"
    ).status == "failed"


def test_failed_analysis_does_not_remain_processing(
    isolated_database,
    tmp_path,
    monkeypatch,
):
    path = tmp_path / "report.pdf"
    path.write_bytes(b"test")

    document = create_document(
        "error-recovery-final",
        path,
    )
    document_service.register(document)

    monkeypatch.setattr(
        report_service,
        "analyze_report",
        lambda file_path, document_id: (
            (_ for _ in ()).throw(
                RuntimeError("Analysis failed.")
            )
        ),
    )

    response = client.post(
        "/api/v1/reports/error-recovery-final/analyze"
    )

    assert response.status_code == 500

    stored_document = document_service.get(
        "error-recovery-final"
    )

    assert stored_document.status != "processing"
    assert stored_document.status == "failed"