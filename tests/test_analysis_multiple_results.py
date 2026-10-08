from ai.analysis.classification import ResultStatus
from ai.analysis.service import ResultAnalysisService
from ai.extraction.schema import (
    ExtractedTestResult,
    ReferenceRange,
    SourceLocation,
)


def make_result(
    test_name,
    value,
    minimum,
    maximum,
):
    return ExtractedTestResult(
        test_name=test_name,
        value=value,
        unit="mg/dL",
        reference_range=ReferenceRange(
            minimum=minimum,
            maximum=maximum,
        ),
        confidence=0.95,
        needs_verification=False,
        source=SourceLocation(
            page=1,
            text=f"{test_name}: {value}",
        ),
    )


def test_analysis_service_handles_multiple_results():
    results = [
        make_result(
            test_name="hemoglobin",
            value=14.0,
            minimum=12.0,
            maximum=16.0,
        ),
        make_result(
            test_name="glucose",
            value=180.0,
            minimum=70.0,
            maximum=140.0,
        ),
        make_result(
            test_name="cholesterol",
            value=120.0,
            minimum=150.0,
            maximum=200.0,
        ),
    ]

    service = ResultAnalysisService()
    analyzed = service.analyze(results)

    assert len(analyzed) == 3

    assert analyzed[0].test_name == "hemoglobin"
    assert analyzed[0].status == ResultStatus.NORMAL

    assert analyzed[1].test_name == "glucose"
    assert analyzed[1].status == ResultStatus.HIGH

    assert analyzed[2].test_name == "cholesterol"
    assert analyzed[2].status == ResultStatus.LOW


def test_analysis_service_preserves_input_order():
    results = [
        make_result(
            test_name="first",
            value=10.0,
            minimum=12.0,
            maximum=16.0,
        ),
        make_result(
            test_name="second",
            value=14.0,
            minimum=12.0,
            maximum=16.0,
        ),
        make_result(
            test_name="third",
            value=18.0,
            minimum=12.0,
            maximum=16.0,
        ),
    ]

    service = ResultAnalysisService()
    analyzed = service.analyze(results)

    assert [result.test_name for result in analyzed] == [
        "first",
        "second",
        "third",
    ]


def test_analysis_service_handles_empty_results():
    service = ResultAnalysisService()

    analyzed = service.analyze([])

    assert analyzed == []