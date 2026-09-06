"""
Patterns used to identify common medical test results.

This module intentionally focuses on extraction only.
It does not decide whether a result is medically dangerous.
"""

import re


NUMBER_PATTERN = r"[-+]?\d+(?:\.\d+)?"

TEST_PATTERNS = {
    "hemoglobin": re.compile(
        rf"\b(?:hemoglobin|haemoglobin|hb)\b"
        rf"\s*[:\-]?\s*({NUMBER_PATTERN})"
        rf"\s*(g/dL|gm/dL|g/L)?",
        re.IGNORECASE,
    ),
    "white_blood_cell_count": re.compile(
        rf"\b(?:white blood cell count|wbc|total leucocyte count|tlc)\b"
        rf"\s*[:\-]?\s*({NUMBER_PATTERN})"
        rf"\s*(?:x\s*10\^?3/?[uµ]?L|10\^?3/?[uµ]?L|cells/?[uµ]?L)?",
        re.IGNORECASE,
    ),
    "platelet_count": re.compile(
        rf"\b(?:platelet count|platelets)\b"
        rf"\s*[:\-]?\s*({NUMBER_PATTERN})"
        rf"\s*(?:x\s*10\^?3/?[uµ]?L|10\^?3/?[uµ]?L|/uL|/?µL)?",
        re.IGNORECASE,
    ),
    "glucose": re.compile(
        rf"\b(?:blood glucose|glucose|blood sugar)\b"
        rf"\s*[:\-]?\s*({NUMBER_PATTERN})"
        rf"\s*(mg/dL|mmol/L)?",
        re.IGNORECASE,
    ),
    "creatinine": re.compile(
        rf"\b(?:serum creatinine|creatinine)\b"
        rf"\s*[:\-]?\s*({NUMBER_PATTERN})"
        rf"\s*(mg/dL|µmol/L|umol/L)?",
        re.IGNORECASE,
    ),
}