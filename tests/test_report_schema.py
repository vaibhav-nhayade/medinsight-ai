import pytest
from pydantic import ValidationError

from backend.schemas.report import (
    AnalysisResponse,
    AnalysisSummaryResponse,
    FindingResponse,
    ReportResultResponse,
)


def make_result(**overrides):
    data = {
        "test_name": "hemoglobin",
        "value": 18.0,
        "unit": "g/dL",
        "reference_minimum": 12.0,
        "reference_maximum": 16.0,
        "status": "high",
        "confidence": 0.95,
        "needs_verification": False,
        "source_page": 2,
    }
    data.update(overrides)
    return ReportResultResponse(**data)


def make_finding(**overrides):
    data = {
        "test_name": "hemoglobin",
        "status": "high",
        "value": 18.0,
        "unit": "g/dL",
        "title": "Hemoglobin is above the reference range",
        "description": "The reported value is above the supplied reference range.",
        "severity": "attention",
        "source_page": 2,
        "needs_verification": False,
    }
    data.update(overrides)
    return FindingResponse(**data)


def make_summary(**overrides):
    data = {
        "total_results": 1,
        "normal_results": 0,
        "low_results": 0,
        "high_results": 1,
        "unknown_results": 0,
        "findings_count": 1,
        "verification_required": 0,
    }
    data.update(overrides)
    return AnalysisSummaryResponse(**data)


def make_response(**overrides):
    data = {
        "document_id": "test-001",
        "filename": "report.pdf",
        "results": [make_result()],
        "findings": [make_finding()],
        "summary": make_summary(),
    }
    data.update(overrides)
    return AnalysisResponse(**data)


def test_result_schema_accepts_valid_data():
    result = make_result()

    assert result.test_name == "hemoglobin"
    assert result.status == "high"
    assert result.confidence == 0.95


def test_result_schema_rejects_confidence_above_one():
    with pytest.raises(ValidationError):
        make_result(confidence=1.1)


def test_result_schema_rejects_negative_confidence():
    with pytest.raises(ValidationError):
        make_result(confidence=-0.1)


def test_result_schema_accepts_boundary_confidence_values():
    assert make_result(confidence=0.0).confidence == 0.0
    assert make_result(confidence=1.0).confidence == 1.0


def test_finding_schema_accepts_valid_data():
    finding = make_finding()

    assert finding.test_name == "hemoglobin"
    assert finding.status == "high"
    assert finding.severity == "attention"


def test_summary_schema_accepts_valid_data():
    summary = make_summary()

    assert summary.total_results == 1
    assert summary.high_results == 1
    assert summary.findings_count == 1


def test_analysis_response_accepts_nested_data():
    response = make_response()

    assert response.document_id == "test-001"
    assert len(response.results) == 1
    assert len(response.findings) == 1
    assert response.summary.total_results == 1


def test_analysis_response_requires_document_id():
    with pytest.raises(ValidationError):
        make_response(document_id=None)


def test_analysis_response_requires_filename():
    with pytest.raises(ValidationError):
        make_response(filename=None)


def test_analysis_response_requires_summary():
    with pytest.raises(ValidationError):
        make_response(summary=None)