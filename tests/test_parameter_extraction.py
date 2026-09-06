from ai.extraction.parameter_extractor import MedicalParameterExtractor
from ai.extraction.validator import validate_extracted_result


def test_extract_hemoglobin():
    text = "Hemoglobin: 13.5 g/dL"

    extractor = MedicalParameterExtractor()
    results = extractor.extract(text)

    assert len(results) == 1
    assert results[0].test_name == "hemoglobin"
    assert results[0].value == 13.5
    assert results[0].unit == "g/dL"


def test_extract_multiple_parameters():
    text = """
    Hemoglobin: 13.5 g/dL
    Glucose: 96 mg/dL
    Creatinine: 0.9 mg/dL
    """

    extractor = MedicalParameterExtractor()
    results = extractor.extract(text)

    names = {result.test_name for result in results}

    assert "hemoglobin" in names
    assert "glucose" in names
    assert "creatinine" in names
    assert len(results) == 3


def test_source_page_is_preserved():
    text = "Glucose: 105 mg/dL"

    extractor = MedicalParameterExtractor()
    results = extractor.extract(
        text,
        page_number=2,
    )

    assert results[0].source.page == 2
    assert results[0].source.text == "Glucose: 105 mg/dL"


def test_invalid_confidence_requires_verification():
    extractor = MedicalParameterExtractor()

    result = extractor.extract(
        "Hemoglobin: 13.5 g/dL"
    )[0]

    result.confidence = 0.50

    validated = validate_extracted_result(result)

    assert validated.needs_verification is True