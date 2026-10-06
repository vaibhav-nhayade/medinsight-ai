from types import SimpleNamespace

from ai.analysis.classification import ResultStatus
from ai.analysis.orchestrator import AnalysisOrchestrator
from ai.extraction.schema import (
    ExtractedTestResult,
    ReferenceRange,
    SourceLocation,
)


def make_result(
    value,
    minimum=None,
    maximum=None,
    test_name="hemoglobin",
):
    return ExtractedTestResult(
        test_name=test_name,
        value=value,
        unit="g/dL",
        reference_range=ReferenceRange(
            minimum=minimum,
            maximum=maximum,
        ),
        confidence=0.95,
        source=SourceLocation(
            page=2,
            text="Hemoglobin: 18.0 g/dL",
        ),
    )


def test_orchestrator_can_be_initialized():
    orchestrator = AnalysisOrchestrator()

    assert orchestrator.report_parser is not None
    assert orchestrator.result_analysis_service is not None
    assert orchestrator.finding_service is not None


def test_orchestrator_runs_complete_analysis_pipeline(monkeypatch):
    orchestrator = AnalysisOrchestrator()

    document = SimpleNamespace(
        document_id="test-001",
        filename="report.pdf",
    )

    extracted_result = make_result(
        value=18.0,
        minimum=12.0,
        maximum=16.0,
    )

    def fake_parse(file_path, document_id):
        assert file_path == "sample.pdf"
        assert document_id == "test-001"
        return document, [extracted_result]

    monkeypatch.setattr(
        orchestrator.report_parser,
        "parse",
        fake_parse,
    )

    analysis = orchestrator.analyze(
        file_path="sample.pdf",
        document_id="test-001",
    )

    assert analysis.document_id == "test-001"
    assert analysis.filename == "report.pdf"

    assert len(analysis.results) == 1
    assert analysis.results[0].status == ResultStatus.HIGH

    assert len(analysis.findings) == 1
    assert analysis.findings[0].status == ResultStatus.HIGH

    assert analysis.summary.total_results == 1
    assert analysis.summary.high_results == 1
    assert analysis.summary.normal_results == 0
    assert analysis.summary.low_results == 0
    assert analysis.summary.unknown_results == 0
    assert analysis.summary.findings_count == 1


def test_orchestrator_handles_normal_result_without_finding(monkeypatch):
    orchestrator = AnalysisOrchestrator()

    document = SimpleNamespace(
        document_id="test-002",
        filename="normal-report.pdf",
    )

    extracted_result = make_result(
        value=14.0,
        minimum=12.0,
        maximum=16.0,
    )

    monkeypatch.setattr(
        orchestrator.report_parser,
        "parse",
        lambda file_path, document_id: (
            document,
            [extracted_result],
        ),
    )

    analysis = orchestrator.analyze(
        file_path="normal-report.pdf",
        document_id="test-002",
    )

    assert analysis.results[0].status == ResultStatus.NORMAL
    assert analysis.findings == []

    assert analysis.summary.total_results == 1
    assert analysis.summary.normal_results == 1
    assert analysis.summary.findings_count == 0