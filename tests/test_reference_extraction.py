from ai.extraction.reference_extractor import ReferenceRangeExtractor
from ai.extraction.result_parser import MedicalResultParser


def test_extract_explicit_reference_range():
    text = "Reference Range: 12.0 - 16.0"

    extractor = ReferenceRangeExtractor()
    result = extractor.extract(text)

    assert result is not None
    assert result.minimum == 12.0
    assert result.maximum == 16.0


def test_extract_reference_range_with_to():
    text = "Normal Range: 70 to 100"

    extractor = ReferenceRangeExtractor()
    result = extractor.extract(text)

    assert result is not None
    assert result.minimum == 70.0
    assert result.maximum == 100.0


def test_missing_reference_range_returns_none():
    text = "Hemoglobin: 13.5 g/dL"

    extractor = ReferenceRangeExtractor()
    result = extractor.extract(text)

    assert result is None


def test_result_parser_attaches_reference_range():
    text = """
    Hemoglobin: 13.5 g/dL
    Reference Range: 12.0 - 16.0
    """

    parser = MedicalResultParser()
    results = parser.parse(text, page_number=1)

    assert len(results) == 1
    assert results[0].test_name == "hemoglobin"
    assert results[0].reference_range.minimum == 12.0
    assert results[0].reference_range.maximum == 16.0


def test_result_without_reference_range_is_not_guessed():
    text = """
    Hemoglobin: 13.5 g/dL
    """

    parser = MedicalResultParser()
    results = parser.parse(text)

    assert len(results) == 1
    assert results[0].reference_range.minimum is None
    assert results[0].reference_range.maximum is None