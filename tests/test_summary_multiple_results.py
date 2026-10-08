from ai.analysis.classification import ResultStatus
from ai.analysis.finding import MedicalFinding
from ai.analysis.result import AnalyzedTestResult
from ai.analysis.summary import build_analysis_summary


def make_result(
    test_name,
    status,
    needs_verification=False,
):
    return AnalyzedTestResult(
        test_name=test_name,
        value=14.0,
        unit="mg/dL",
        reference_minimum=12.0,
        reference_maximum=16.0,
        status=status,
        confidence=0.95,
        needs_verification=needs_verification,
        source_page=1,
        source_text=f"{test_name}: 14.0",
    )


def make_finding(test_name, status):
    return MedicalFinding(
        test_name=test_name,
        status=status,
        value=18.0,
        unit="mg/dL",
        reference_minimum=12.0,
        reference_maximum=16.0,
        title=f"{test_name} requires attention",
        description="The reported result requires attention.",
        severity="attention",
        source_page=1,
        needs_verification=False,
    )


def test_summary_aggregates_mixed_results():
    results = [
        make_result("normal-1", ResultStatus.NORMAL),
        make_result("normal-2", ResultStatus.NORMAL),
        make_result("high-1", ResultStatus.HIGH),
        make_result("high-2", ResultStatus.HIGH),
        make_result("low-1", ResultStatus.LOW),
        make_result("unknown-1", ResultStatus.UNKNOWN),
    ]

    findings = [
        make_finding("high-1", ResultStatus.HIGH),
        make_finding("high-2", ResultStatus.HIGH),
        make_finding("low-1", ResultStatus.LOW),
        make_finding("unknown-1", ResultStatus.UNKNOWN),
    ]

    summary = build_analysis_summary(
        results=results,
        findings=findings,
    )

    assert summary.total_results == 6
    assert summary.normal_results == 2
    assert summary.high_results == 2
    assert summary.low_results == 1
    assert summary.unknown_results == 1
    assert summary.findings_count == 4


def test_summary_counts_multiple_verification_flags():
    results = [
        make_result(
            "verified-1",
            ResultStatus.HIGH,
            needs_verification=False,
        ),
        make_result(
            "verify-1",
            ResultStatus.HIGH,
            needs_verification=True,
        ),
        make_result(
            "verify-2",
            ResultStatus.UNKNOWN,
            needs_verification=True,
        ),
        make_result(
            "verified-2",
            ResultStatus.NORMAL,
            needs_verification=False,
        ),
    ]

    summary = build_analysis_summary(
        results=results,
        findings=[],
    )

    assert summary.total_results == 4
    assert summary.verification_required == 2