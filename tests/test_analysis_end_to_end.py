from pathlib import Path

from fastapi.testclient import TestClient

from ai.analysis.classification import ResultStatus
from ai.analysis.finding import MedicalFinding
from ai.analysis.orchestrator import ReportAnalysis
from ai.analysis.result import AnalyzedTestResult
from ai.analysis.summary import AnalysisSummary
from backend.main import app
from backend.models.document import DocumentRecord
from backend.routes.analysis import report_service
from backend.services.document_service import document_service


client = TestClient(app)


def make_analysis(document_id):
    result = AnalyzedTestResult(
        test_name="hemoglobin",
        value=18.0,
        unit="g/dL",
        reference_minimum=12.0,
        reference_maximum=16.0,
        status=ResultStatus.HIGH,
        confidence=0.95,
        needs_verification=False,
        source_page=1,
        source_text="Hemoglobin: 18.0 g/dL",
    )

    finding = MedicalFinding(
        test_name="hemoglobin",
        status=ResultStatus.HIGH,
        value=18.0,
        unit="g/dL",
        reference_minimum=12.0,
        reference_maximum=16.0,
        title="Hemoglobin is above the reported range",
        description="The reported result is above the reference range.",
        severity="attention",
        source_page=1,
        needs_verification=False,
    )

    summary = AnalysisSummary(
        total_results=1,
        normal_results=0,
        low_results=0,
        high_results=1,
        unknown_results=0,
        findings_count=1,
        verification_required=0,
    )

    return ReportAnalysis(
        document_id=document_id,
        filename="blood_report.pdf",
        results=[result],
        findings=[finding],
        summary=summary,
    )


def test_end_to_end_analysis_flow(
    isolated_database,
    tmp_path,
    monkeypatch,
):
    document_path = tmp_path / "blood_report.pdf"
    document_path.write_bytes(b"test pdf")

    document = DocumentRecord(
        document_id="e2e-001",
        original_filename="blood_report.pdf",
        file_type="pdf",
        size_bytes=4096,
        storage_path=Path(document_path),
    )

    document_service.register(document)

    expected_analysis = make_analysis("e2e-001")

    monkeypatch.setattr(
        report_service.analysis_orchestrator,
        "analyze",
        lambda file_path, document_id: expected_analysis,
    )

    response = client.post(
        "/api/v1/reports/e2e-001/analyze"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_id"] == "e2e-001"
    assert data["filename"] == "blood_report.pdf"

    assert len(data["results"]) == 1
    assert data["results"][0]["test_name"] == "hemoglobin"
    assert data["results"][0]["status"] == "high"
    assert data["results"][0]["value"] == 18.0

    assert len(data["findings"]) == 1
    assert data["findings"][0]["test_name"] == "hemoglobin"
    assert data["findings"][0]["status"] == "high"
    assert data["findings"][0]["severity"] == "attention"

    assert data["summary"]["total_results"] == 1
    assert data["summary"]["high_results"] == 1
    assert data["summary"]["findings_count"] == 1

    stored_document = document_service.get("e2e-001")

    assert stored_document.status == "processed"