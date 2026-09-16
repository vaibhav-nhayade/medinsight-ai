from pathlib import Path

from ai.analysis.orchestrator import AnalysisOrchestrator


def create_sample_report(tmp_path: Path) -> Path:
    """
    Create a minimal PDF-like test fixture.

    The orchestrator itself expects a PDF, so this test is skipped
    when a PDF fixture cannot be created by the available environment.
    """
    return tmp_path / "sample.pdf"


def test_orchestrator_can_be_initialized():
    orchestrator = AnalysisOrchestrator()

    assert orchestrator.report_parser is not None
    assert orchestrator.finding_service is not None


def test_report_analysis_dataclass():
    from ai.analysis.orchestrator import ReportAnalysis
    from ai.analysis.summary import AnalysisSummary

    summary = AnalysisSummary(
        total_results=1,
        normal_results=0,
        low_results=0,
        high_results=1,
        unknown_results=0,
        findings_count=1,
        verification_required=0,
    )

    analysis = ReportAnalysis(
        document_id="test-001",
        filename="report.pdf",
        results=[],
        findings=[],
        summary=summary,
    )

    assert analysis.document_id == "test-001"
    assert analysis.filename == "report.pdf"
    assert analysis.summary.high_results == 1