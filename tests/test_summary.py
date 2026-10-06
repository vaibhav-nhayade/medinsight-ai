from ai.analysis.classification import ResultStatus
from ai.analysis.finding import MedicalFinding
from ai.analysis.result import AnalyzedTestResult
from ai.analysis.summary import build_analysis_summary


def make_result(
    status,
    needs_verification=False,
    test_name="hemoglobin",
):
    return AnalyzedTestResult(
        test_name=test_name,
        value=14.0,
        unit="g/dL",
        reference_minimum=12.0,
        reference_maximum=16.0,
        status=status,
        confidence=0.95,
        needs_verification=needs_verification,
        source_page=1,
        source_text="sample",
    )


def make_finding(status):
    return MedicalFinding(
        test_name="hemoglobin",
        status=status,
        value=18.0,
        unit="g/dL",
        reference_minimum=12.0,
        reference_maximum=16.0,
        title="Hemoglobin is above the reference range",
        description="The reported value is above the supplied reference range.",
        severity="attention",
        source_page=1,
        needs_verification=False,
    )


def test_summary_counts_all_result_statuses():
    results = [
        make_result(ResultStatus.NORMAL, test_name="hemoglobin"),
        make_result(ResultStatus.LOW, test_name="platelets"),
        make_result(ResultStatus.HIGH, test_name="glucose"),
        make_result(ResultStatus.UNKNOWN, test_name="vitamin_d"),
    ]

    summary = build_analysis_summary(
        results=results,
        findings=[],
    )

    assert summary.total_results == 4
    assert summary.normal_results == 1
    assert summary.low_results == 1
    assert summary.high_results == 1
    assert summary.unknown_results == 1


def test_summary_counts_findings():
    results = [
        make_result(ResultStatus.HIGH),
        make_result(ResultStatus.LOW, test_name="platelets"),
    ]

    findings = [
        make_finding(ResultStatus.HIGH),
        make_finding(ResultStatus.LOW),
    ]

    summary = build_analysis_summary(
        results=results,
        findings=findings,
    )

    assert summary.findings_count == 2


def test_summary_counts_verification_required():
    results = [
        make_result(
            ResultStatus.HIGH,
            needs_verification=True,
        ),
        make_result(
            ResultStatus.NORMAL,
            needs_verification=False,
            test_name="glucose",
        ),
        make_result(
            ResultStatus.UNKNOWN,
            needs_verification=True,
            test_name="vitamin_d",
        ),
    ]

    summary = build_analysis_summary(
        results=results,
        findings=[],
    )

    assert summary.verification_required == 2


def test_summary_handles_empty_analysis():
    summary = build_analysis_summary(
        results=[],
        findings=[],
    )

    assert summary.total_results == 0
    assert summary.normal_results == 0
    assert summary.low_results == 0
    assert summary.high_results == 0
    assert summary.unknown_results == 0
    assert summary.findings_count == 0
    assert summary.verification_required == 0