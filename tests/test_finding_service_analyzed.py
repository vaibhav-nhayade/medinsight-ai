from ai.analysis.classification import ResultStatus
from ai.analysis.finding_service import FindingService
from ai.analysis.result import AnalyzedTestResult


def make_analyzed_result(
    status,
    value=18.0,
    needs_verification=False,
):
    return AnalyzedTestResult(
        test_name="hemoglobin",
        value=value,
        unit="g/dL",
        reference_minimum=12.0,
        reference_maximum=16.0,
        status=status,
        confidence=0.95,
        needs_verification=needs_verification,
        source_page=2,
        source_text="Hemoglobin: 18.0 g/dL",
    )


def test_finding_service_accepts_analyzed_high_result():
    result = make_analyzed_result(ResultStatus.HIGH)

    service = FindingService()
    findings = service.generate_findings([result])

    assert len(findings) == 1
    assert findings[0].status == ResultStatus.HIGH
    assert findings[0].value == 18.0
    assert findings[0].source_page == 2


def test_finding_service_accepts_analyzed_low_result():
    result = make_analyzed_result(
        ResultStatus.LOW,
        value=10.0,
    )

    service = FindingService()
    findings = service.generate_findings([result])

    assert len(findings) == 1
    assert findings[0].status == ResultStatus.LOW
    assert findings[0].value == 10.0


def test_finding_service_omits_analyzed_normal_result():
    result = make_analyzed_result(
        ResultStatus.NORMAL,
        value=14.0,
    )

    service = FindingService()
    findings = service.generate_findings([result])

    assert findings == []


def test_finding_service_marks_analyzed_unknown_result_for_verification():
    result = make_analyzed_result(
        ResultStatus.UNKNOWN,
        needs_verification=True,
    )

    service = FindingService()
    findings = service.generate_findings([result])

    assert len(findings) == 1
    assert findings[0].status == ResultStatus.UNKNOWN
    assert findings[0].severity == "verification"
    assert findings[0].needs_verification is True


def test_finding_service_preserves_analyzed_result_metadata():
    result = make_analyzed_result(
        ResultStatus.HIGH,
        needs_verification=True,
    )

    service = FindingService()
    findings = service.generate_findings([result])

    finding = findings[0]

    assert finding.test_name == "hemoglobin"
    assert finding.unit == "g/dL"
    assert finding.reference_minimum == 12.0
    assert finding.reference_maximum == 16.0
    assert finding.source_page == 2
    assert finding.needs_verification is True