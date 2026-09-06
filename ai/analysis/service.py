"""
Service responsible for deterministic medical result analysis.
"""

from ai.extraction.schema import ExtractedTestResult

from .classification import ResultStatus, classify_result
from .result import AnalyzedTestResult, build_analyzed_result


class ResultAnalysisService:
    """Analyze extracted results against supplied reference ranges."""

    def analyze(
        self,
        results: list[ExtractedTestResult],
    ) -> list[AnalyzedTestResult]:

        analyzed_results: list[AnalyzedTestResult] = []

        for result in results:
            status: ResultStatus = classify_result(
                value=result.value,
                reference_range=result.reference_range,
            )

            analyzed_results.append(
                build_analyzed_result(
                    result=result,
                    status=status,
                )
            )

        return analyzed_results