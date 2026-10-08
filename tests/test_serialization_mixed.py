from ai.analysis.classification import ResultStatus
from ai.analysis.finding import MedicalFinding
from ai.analysis.orchestrator import ReportAnalysis
from ai.analysis.result import AnalyzedTestResult
from ai.analysis.serialization import analysis_to_dict
from ai.analysis.summary import AnalysisSummary


def make_result(test_name, status, value):
    return AnalyzedTestResult(
        test_name=test_name,
        value=value,
        unit="mg/dL",
        reference_minimum=12.0,
        reference_maximum=16.0,
        status=status,
        confidence=0.95,
        needs_verification=status == ResultStatus.UNKNOWN,
        source_page=1,
        source_text=f"{test_name}: {value}",
    )


def make_finding(test_name, status, value):
    return MedicalFinding(
        test_name=test_name,
        status=status,
        value=value,
        unit="mg/dL",
        reference_minimum=12.0,
        reference_maximum=16.0,
        title=f"{test_name} requires attention",
        description="The reported result requires attention.",
        severity=(
            "verification"
            if status == ResultStatus.UNKNOWN
            else "attention"
        ),
        source_page=1,
        needs_verification=status == ResultStatus.UNKNOWN,
    )


def make_analysis():
    results = [
        make_result(
            "normal-test",
            ResultStatus.NORMAL,
            14.0,
        ),
        make_result(
            "high-test",
            ResultStatus.HIGH,
            18.0,
        ),
        make_result(
            "low-test",
            ResultStatus.LOW,
            10.0,
        ),
        make_result(
            "unknown-test",
            ResultStatus.UNKNOWN,
            14.0,
        ),
    ]

    findings = [
        make_finding(
            "high-test",
            ResultStatus.HIGH,
            18.0,
        ),
        make_finding(
            "low-test",
            ResultStatus.LOW,
            10.0,
        ),
        make_finding(
            "unknown-test",
            ResultStatus.UNKNOWN,
            14.0,
        ),
    ]

    summary = AnalysisSummary(
        total_results=4,
        normal_results=1,
        low_results=1,
        high_results=1,
        unknown_results=1,
        findings_count=3,
        verification_required=1,
    )

    return ReportAnalysis(
        document_id="mixed-001",
        filename="mixed-report.pdf",
        results=results,
        findings=findings,
        summary=summary,
    )


def test_serialization_preserves_all_results():
    data = analysis_to_dict(make_analysis())

    assert len(data["results"]) == 4

    assert data["results"][0]["test_name"] == "normal-test"
    assert data["results"][1]["test_name"] == "high-test"
    assert data["results"][2]["test_name"] == "low-test"
    assert data["results"][3]["test_name"] == "unknown-test"


def test_serialization_preserves_result_statuses():
    data = analysis_to_dict(make_analysis())

    assert data["results"][0]["status"] == ResultStatus.NORMAL
    assert data["results"][1]["status"] == ResultStatus.HIGH
    assert data["results"][2]["status"] == ResultStatus.LOW
    assert data["results"][3]["status"] == ResultStatus.UNKNOWN


def test_serialization_preserves_findings():
    data = analysis_to_dict(make_analysis())

    assert len(data["findings"]) == 3

    assert data["findings"][0]["test_name"] == "high-test"
    assert data["findings"][1]["test_name"] == "low-test"
    assert data["findings"][2]["test_name"] == "unknown-test"


def test_serialization_preserves_summary_counts():
    data = analysis_to_dict(make_analysis())

    summary = data["summary"]

    assert summary["total_results"] == 4
    assert summary["normal_results"] == 1
    assert summary["low_results"] == 1
    assert summary["high_results"] == 1
    assert summary["unknown_results"] == 1
    assert summary["findings_count"] == 3
    assert summary["verification_required"] == 1