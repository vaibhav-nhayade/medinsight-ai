from ai.analysis.analysis_schema import (
    AnalysisReport,
    AnalysisResultItem,
)
from ai.analysis.classification import ResultStatus


def make_result_item(**overrides):
    data = {
        "test_name": "hemoglobin",
        "value": 18.0,
        "unit": "g/dL",
        "status": ResultStatus.HIGH,
        "reference_minimum": 12.0,
        "reference_maximum": 16.0,
        "confidence": 0.95,
        "needs_verification": False,
        "source_page": 2,
    }
    data.update(overrides)
    return AnalysisResultItem(**data)


def test_analysis_result_item_preserves_all_fields():
    result = make_result_item()

    assert result.test_name == "hemoglobin"
    assert result.value == 18.0
    assert result.unit == "g/dL"
    assert result.status == ResultStatus.HIGH
    assert result.reference_minimum == 12.0
    assert result.reference_maximum == 16.0
    assert result.confidence == 0.95
    assert result.needs_verification is False
    assert result.source_page == 2


def test_analysis_result_item_supports_unknown_result():
    result = make_result_item(
        value=None,
        status=ResultStatus.UNKNOWN,
        reference_minimum=None,
        reference_maximum=None,
        needs_verification=True,
    )

    assert result.value is None
    assert result.status == ResultStatus.UNKNOWN
    assert result.reference_minimum is None
    assert result.reference_maximum is None
    assert result.needs_verification is True


def test_analysis_report_preserves_report_metadata():
    result = make_result_item()

    report = AnalysisReport(
        document_id="test-001",
        filename="report.pdf",
        results=[result],
        finding_count=1,
        verification_required=0,
    )

    assert report.document_id == "test-001"
    assert report.filename == "report.pdf"
    assert len(report.results) == 1
    assert report.finding_count == 1
    assert report.verification_required == 0


def test_analysis_report_supports_empty_results():
    report = AnalysisReport(
        document_id="test-002",
        filename="empty.pdf",
        results=[],
        finding_count=0,
        verification_required=0,
    )

    assert report.results == []
    assert report.finding_count == 0
    assert report.verification_required == 0