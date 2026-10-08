from ai.analysis.classification import ResultStatus
from ai.analysis.finding import MedicalFinding
from ai.analysis.orchestrator import ReportAnalysis
from ai.analysis.result import AnalyzedTestResult
from ai.analysis.serialization import analysis_to_dict
from ai.analysis.summary import AnalysisSummary


def make_analysis():
    result = AnalyzedTestResult(
        test_name="hemoglobin",
        value=18.0,
        unit="g/dL",
        reference_minimum=12.0,
        reference_maximum=16.0,
        status=ResultStatus.HIGH,
        confidence=0.95,
        needs_verification=False,
        source_page=2,
        source_text="Hemoglobin: 18.0 g/dL",
    )

    finding = MedicalFinding(
        test_name="hemoglobin",
        status=ResultStatus.HIGH,
        value=18.0,
        unit="g/dL",
        reference_minimum=12.0,
        reference_maximum=16.0,
        title="Hemoglobin is above the reference range",
        description="The reported value is above the supplied reference range.",
        severity="attention",
        source_page=2,
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
        document_id="test-001",
        filename="report.pdf",
        results=[result],
        findings=[finding],
        summary=summary,
    )


def test_analysis_to_dict_preserves_top_level_fields():
    analysis = make_analysis()

    data = analysis_to_dict(analysis)

    assert data["document_id"] == "test-001"
    assert data["filename"] == "report.pdf"


def test_analysis_to_dict_serializes_result():
    analysis = make_analysis()

    data = analysis_to_dict(analysis)

    assert len(data["results"]) == 1

    result = data["results"][0]

    assert result["test_name"] == "hemoglobin"
    assert result["value"] == 18.0
    assert result["unit"] == "g/dL"
    assert result["reference_minimum"] == 12.0
    assert result["reference_maximum"] == 16.0
    assert result["status"] == ResultStatus.HIGH
    assert result["confidence"] == 0.95
    assert result["needs_verification"] is False
    assert result["source_page"] == 2


def test_analysis_to_dict_serializes_finding():
    analysis = make_analysis()

    data = analysis_to_dict(analysis)

    assert len(data["findings"]) == 1

    finding = data["findings"][0]

    assert finding["test_name"] == "hemoglobin"
    assert finding["status"] == ResultStatus.HIGH
    assert finding["value"] == 18.0
    assert finding["title"] == "Hemoglobin is above the reference range"
    assert finding["severity"] == "attention"
    assert finding["source_page"] == 2


def test_analysis_to_dict_serializes_summary():
    analysis = make_analysis()

    data = analysis_to_dict(analysis)

    summary = data["summary"]

    assert summary["total_results"] == 1
    assert summary["normal_results"] == 0
    assert summary["low_results"] == 0
    assert summary["high_results"] == 1
    assert summary["unknown_results"] == 0
    assert summary["findings_count"] == 1
    assert summary["verification_required"] == 0