from ai.analysis.classification import ResultStatus
from ai.analysis.service import ResultAnalysisService
from ai.extraction.schema import (
    ExtractedTestResult,
    ReferenceRange,
    SourceLocation,
)


def make_result(
    value,
    minimum=None,
    maximum=None,
    needs_verification=False,
):
    return ExtractedTestResult(
        test_name="hemoglobin",
        value=value,
        unit="g/dL",
        reference_range=ReferenceRange(
            minimum=minimum,
            maximum=maximum,
        ),
        confidence=0.95,
        needs_verification=needs_verification,
        source=SourceLocation(
            page=3,
            text="Hemoglobin result",
        ),
    )


def analyze(result):
    service = ResultAnalysisService()
    return service.analyze([result])[0]


def test_lower_reference_boundary_is_normal():
    analyzed = analyze(
        make_result(
            value=12.0,
            minimum=12.0,
            maximum=16.0,
        )
    )

    assert analyzed.status == ResultStatus.NORMAL


def test_upper_reference_boundary_is_normal():
    analyzed = analyze(
        make_result(
            value=16.0,
            minimum=12.0,
            maximum=16.0,
        )
    )

    assert analyzed.status == ResultStatus.NORMAL


def test_missing_value_is_unknown():
    analyzed = analyze(
        make_result(
            value=None,
            minimum=12.0,
            maximum=16.0,
        )
    )

    assert analyzed.status == ResultStatus.UNKNOWN


def test_lower_only_reference_range():
    analyzed = analyze(
        make_result(
            value=10.0,
            minimum=12.0,
        )
    )

    assert analyzed.status == ResultStatus.LOW


def test_upper_only_reference_range():
    analyzed = analyze(
        make_result(
            value=18.0,
            maximum=16.0,
        )
    )

    assert analyzed.status == ResultStatus.HIGH


def test_verification_flag_is_preserved():
    analyzed = analyze(
        make_result(
            value=18.0,
            minimum=12.0,
            maximum=16.0,
            needs_verification=True,
        )
    )

    assert analyzed.status == ResultStatus.HIGH
    assert analyzed.needs_verification is True
    assert analyzed.source_page == 3