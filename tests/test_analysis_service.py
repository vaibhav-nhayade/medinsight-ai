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
            page=2,
            text="Hemoglobin: 18.0 g/dL",
        ),
    )


def test_analysis_service_classifies_high_result():
    result = make_result(
        value=18.0,
        minimum=12.0,
        maximum=16.0,
    )

    service = ResultAnalysisService()
    analyzed = service.analyze([result])

    assert len(analyzed) == 1
    assert analyzed[0].status == ResultStatus.HIGH


def test_analysis_service_classifies_low_result():
    result = make_result(
        value=10.0,
        minimum=12.0,
        maximum=16.0,
    )

    service = ResultAnalysisService()
    analyzed = service.analyze([result])

    assert len(analyzed) == 1
    assert analyzed[0].status == ResultStatus.LOW


def test_analysis_service_classifies_normal_result():
    result = make_result(
        value=14.0,
        minimum=12.0,
        maximum=16.0,
    )

    service = ResultAnalysisService()
    analyzed = service.analyze([result])

    assert len(analyzed) == 1
    assert analyzed[0].status == ResultStatus.NORMAL


def test_analysis_service_handles_unknown_result():
    result = make_result(value=14.0)

    service = ResultAnalysisService()
    analyzed = service.analyze([result])

    assert len(analyzed) == 1
    assert analyzed[0].status == ResultStatus.UNKNOWN


def test_analysis_service_preserves_result_metadata():
    result = make_result(
        value=18.0,
        minimum=12.0,
        maximum=16.0,
    )

    service = ResultAnalysisService()
    analyzed = service.analyze([result])

    assert analyzed[0].test_name == "hemoglobin"
    assert analyzed[0].value == 18.0
    assert analyzed[0].unit == "g/dL"
    assert analyzed[0].reference_minimum == 12.0
    assert analyzed[0].reference_maximum == 16.0
    assert analyzed[0].confidence == 0.95
    assert analyzed[0].needs_verification is False
    assert analyzed[0].source_page == 2
    assert analyzed[0].source_text == "Hemoglobin: 18.0 g/dL"