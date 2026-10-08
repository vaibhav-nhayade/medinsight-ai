from ai.analysis.classification import ResultStatus
from ai.analysis.finding_rules import (
    build_finding_description,
    build_finding_title,
)


def test_high_finding_title():
    title = build_finding_title(
        test_name="hemoglobin",
        status=ResultStatus.HIGH,
    )

    assert "Hemoglobin" in title
    assert "above" in title.lower()
    assert "range" in title.lower()


def test_low_finding_title():
    title = build_finding_title(
        test_name="hemoglobin",
        status=ResultStatus.LOW,
    )

    assert "Hemoglobin" in title
    assert "below" in title.lower()
    assert "range" in title.lower()


def test_unknown_finding_title():
    title = build_finding_title(
        test_name="hemoglobin",
        status=ResultStatus.UNKNOWN,
    )

    assert "Hemoglobin" in title
    assert (
        "classif" in title.lower()
        or "verif" in title.lower()
    )


def test_high_finding_description():
    description = build_finding_description(
        test_name="hemoglobin",
        status=ResultStatus.HIGH,
        value=18.0,
        unit="g/dL",
        minimum=12.0,
        maximum=16.0,
    )

    assert "Hemoglobin" in description
    assert "18" in description
    assert "g/dL" in description
    assert "above" in description.lower()
    assert "reference range" in description.lower()


def test_low_finding_description():
    description = build_finding_description(
        test_name="hemoglobin",
        status=ResultStatus.LOW,
        value=10.0,
        unit="g/dL",
        minimum=12.0,
        maximum=16.0,
    )

    assert "Hemoglobin" in description
    assert "10" in description
    assert "g/dL" in description
    assert "below" in description.lower()
    assert "reference range" in description.lower()


def test_unknown_finding_description():
    description = build_finding_description(
        test_name="vitamin_d",
        status=ResultStatus.UNKNOWN,
        value=14.0,
        unit="ng/mL",
        minimum=None,
        maximum=None,
    )

    assert "Vitamin D" in description
    assert "14" in description
    assert "ng/mL" in description
    assert "reference-range" in description.lower()
    assert "classif" in description.lower()