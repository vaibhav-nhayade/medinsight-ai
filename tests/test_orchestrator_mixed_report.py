from types import SimpleNamespace

from ai.analysis.classification import ResultStatus
from ai.analysis.orchestrator import AnalysisOrchestrator
from ai.extraction.schema import (
    ExtractedTestResult,
    ReferenceRange,
    SourceLocation,
)


def make_result(
    test_name,
    value,
    minimum=None,
    maximum=None,
):
    return ExtractedTestResult(
        test_name=test_name,
        value=value,
        unit="mg/dL",
        reference_range=ReferenceRange(
            minimum=minimum,
            maximum=maximum,
        ),
        confidence=0.95,
        needs_verification=False,
        source=SourceLocation(
            page=1,
            text=f"{test_name}: {value}",
        ),
    )


def test_orchestrator_handles_mixed_report(monkeypatch):
    orchestrator = AnalysisOrchestrator()

    document = SimpleNamespace(
        document_id="mixed-001",
        filename="mixed-report.pdf",
    )

    extracted_results = [
        make_result(
            "normal-test",
            14.0,
            minimum=12.0,
            maximum=16.0,
        ),
        make_result(
            "high-test",
            180.0,
            minimum=70.0,
            maximum=140.0,
        ),
        make_result(
            "low-test",
            50.0,
            minimum=70.0,
            maximum=140.0,
        ),
        make_result(
            "unknown-test",
            100.0,
        ),
    ]

    monkeypatch.setattr(
        orchestrator.report_parser,
        "parse",
        lambda file_path, document_id: (
            document,
            extracted_results,
        ),
    )

    analysis = orchestrator.analyze(
        file_path="mixed-report.pdf",
        document_id="mixed-001",
    )

    assert analysis.document_id == "mixed-001"
    assert analysis.filename == "mixed-report.pdf"

    assert len(analysis.results) == 4

    assert analysis.results[0].status == ResultStatus.NORMAL
    assert analysis.results[1].status == ResultStatus.HIGH
    assert analysis.results[2].status == ResultStatus.LOW
    assert analysis.results[3].status == ResultStatus.UNKNOWN

    assert len(analysis.findings) == 3

    assert analysis.findings[0].test_name == "high-test"
    assert analysis.findings[0].status == ResultStatus.HIGH

    assert analysis.findings[1].test_name == "low-test"
    assert analysis.findings[1].status == ResultStatus.LOW

    assert analysis.findings[2].test_name == "unknown-test"
    assert analysis.findings[2].status == ResultStatus.UNKNOWN

    assert analysis.summary.total_results == 4
    assert analysis.summary.normal_results == 1
    assert analysis.summary.high_results == 1
    assert analysis.summary.low_results == 1
    assert analysis.summary.unknown_results == 1
    assert analysis.summary.findings_count == 3


def test_orchestrator_preserves_result_order(monkeypatch):
    orchestrator = AnalysisOrchestrator()

    document = SimpleNamespace(
        document_id="order-001",
        filename="order-report.pdf",
    )

    extracted_results = [
        make_result(
            "first",
            18.0,
            minimum=12.0,
            maximum=16.0,
        ),
        make_result(
            "second",
            14.0,
            minimum=12.0,
            maximum=16.0,
        ),
        make_result(
            "third",
            10.0,
            minimum=12.0,
            maximum=16.0,
        ),
    ]

    monkeypatch.setattr(
        orchestrator.report_parser,
        "parse",
        lambda file_path, document_id: (
            document,
            extracted_results,
        ),
    )

    analysis = orchestrator.analyze(
        file_path="order-report.pdf",
        document_id="order-001",
    )

    assert [
        result.test_name
        for result in analysis.results
    ] == [
        "first",
        "second",
        "third",
    ]

    assert [
        finding.test_name
        for finding in analysis.findings
    ] == [
        "first",
        "third",
    ]