from ai.analysis.classification import ResultStatus
from ai.analysis.finding_service import FindingService
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
            page=1,
            text="sample",
        ),
    )


def test_high_result_creates_finding():
    result = make_result(
        value=18.0,
        minimum=12.0,
        maximum=16.0,
    )

    service = FindingService()
    findings = service.generate_findings([result])

    assert len(findings) == 1
    assert findings[0].status == ResultStatus.HIGH
    assert findings[0].severity == "attention"
    assert "above" in findings[0].title.lower()


def test_low_result_creates_finding():
    result = make_result(
        value=10.0,
        minimum=12.0,
        maximum=16.0,
    )

    service = FindingService()
    findings = service.generate_findings([result])

    assert len(findings) == 1
    assert findings[0].status == ResultStatus.LOW
    assert findings[0].severity == "attention"
    assert "below" in findings[0].title.lower()


def test_normal_result_is_not_notable_finding():
    result = make_result(
        value=14.0,
        minimum=12.0,
        maximum=16.0,
    )

    service = FindingService()
    findings = service.generate_findings([result])

    assert findings == []


def test_missing_reference_range_requires_verification():
    result = make_result(
        value=14.0,
    )

    service = FindingService()
    findings = service.generate_findings([result])

    assert len(findings) == 1
    assert findings[0].status == ResultStatus.UNKNOWN
    assert findings[0].severity == "verification"


def test_finding_preserves_source_page():
    result = make_result(
        value=18.0,
        minimum=12.0,
        maximum=16.0,
    )

    service = FindingService()
    findings = service.generate_findings([result])

    assert findings[0].source_page == 1