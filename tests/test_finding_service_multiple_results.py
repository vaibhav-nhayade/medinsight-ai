from ai.analysis.classification import ResultStatus
from ai.analysis.finding_service import FindingService
from ai.analysis.result import AnalyzedTestResult


def make_result(test_name, status, value=14.0):
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


def test_finding_service_handles_mixed_results():
    results = [
        make_result(
            "normal",
            ResultStatus.NORMAL,
            value=14.0,
        ),
        make_result(
            "high",
            ResultStatus.HIGH,
            value=18.0,
        ),
        make_result(
            "low",
            ResultStatus.LOW,
            value=10.0,
        ),
        make_result(
            "unknown",
            ResultStatus.UNKNOWN,
            value=14.0,
        ),
    ]

    service = FindingService()
    findings = service.generate_findings(results)

    assert len(findings) == 3

    assert findings[0].test_name == "high"
    assert findings[0].status == ResultStatus.HIGH

    assert findings[1].test_name == "low"
    assert findings[1].status == ResultStatus.LOW

    assert findings[2].test_name == "unknown"
    assert findings[2].status == ResultStatus.UNKNOWN


def test_finding_service_preserves_finding_order():
    results = [
        make_result(
            "first-high",
            ResultStatus.HIGH,
            value=18.0,
        ),
        make_result(
            "normal",
            ResultStatus.NORMAL,
            value=14.0,
        ),
        make_result(
            "second-high",
            ResultStatus.HIGH,
            value=20.0,
        ),
    ]

    service = FindingService()
    findings = service.generate_findings(results)

    assert [finding.test_name for finding in findings] == [
        "first-high",
        "second-high",
    ]


def test_finding_service_returns_empty_for_all_normal_results():
    results = [
        make_result("normal-1", ResultStatus.NORMAL),
        make_result("normal-2", ResultStatus.NORMAL),
        make_result("normal-3", ResultStatus.NORMAL),
    ]

    service = FindingService()
    findings = service.generate_findings(results)

    assert findings == []