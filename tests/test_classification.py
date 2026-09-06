from ai.analysis.classification import (
    ResultStatus,
    classify_result,
)
from ai.extraction.schema import ReferenceRange


def test_normal_result():
    reference_range = ReferenceRange(
        minimum=12.0,
        maximum=16.0,
    )

    result = classify_result(
        value=14.0,
        reference_range=reference_range,
    )

    assert result == ResultStatus.NORMAL


def test_low_result():
    reference_range = ReferenceRange(
        minimum=12.0,
        maximum=16.0,
    )

    result = classify_result(
        value=10.5,
        reference_range=reference_range,
    )

    assert result == ResultStatus.LOW


def test_high_result():
    reference_range = ReferenceRange(
        minimum=12.0,
        maximum=16.0,
    )

    result = classify_result(
        value=18.0,
        reference_range=reference_range,
    )

    assert result == ResultStatus.HIGH


def test_boundary_values_are_normal():
    reference_range = ReferenceRange(
        minimum=12.0,
        maximum=16.0,
    )

    assert classify_result(
        value=12.0,
        reference_range=reference_range,
    ) == ResultStatus.NORMAL

    assert classify_result(
        value=16.0,
        reference_range=reference_range,
    ) == ResultStatus.NORMAL


def test_missing_reference_range_is_unknown():
    reference_range = ReferenceRange()

    result = classify_result(
        value=14.0,
        reference_range=reference_range,
    )

    assert result == ResultStatus.UNKNOWN


def test_missing_value_is_unknown():
    reference_range = ReferenceRange(
        minimum=12.0,
        maximum=16.0,
    )

    result = classify_result(
        value=None,
        reference_range=reference_range,
    )

    assert result == ResultStatus.UNKNOWN


def test_one_sided_lower_range():
    reference_range = ReferenceRange(
        minimum=12.0,
    )

    assert classify_result(
        value=15.0,
        reference_range=reference_range,
    ) == ResultStatus.NORMAL

    assert classify_result(
        value=10.0,
        reference_range=reference_range,
    ) == ResultStatus.LOW


def test_one_sided_upper_range():
    reference_range = ReferenceRange(
        maximum=16.0,
    )

    assert classify_result(
        value=15.0,
        reference_range=reference_range,
    ) == ResultStatus.NORMAL

    assert classify_result(
        value=18.0,
        reference_range=reference_range,
    ) == ResultStatus.HIGH