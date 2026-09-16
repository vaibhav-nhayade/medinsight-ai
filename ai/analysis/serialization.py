"""
Serialization helpers for analysis results.

The API layer will use these structures later when exposing
analysis results to the frontend.
"""

from dataclasses import asdict
from typing import Any

from .orchestrator import ReportAnalysis


def analysis_to_dict(
    analysis: ReportAnalysis,
) -> dict[str, Any]:
    """Convert a report analysis into JSON-compatible data."""

    data = asdict(analysis)

    data["summary"]["normal_results"] = (
        analysis.summary.normal_results
    )

    return data