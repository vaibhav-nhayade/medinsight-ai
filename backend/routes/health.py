"""
Health and service-status endpoints.
"""

from datetime import datetime, timezone

from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1",
    tags=["Health"],
)


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return backend health information."""

    return {
        "status": "healthy",
        "service": "medinsight-ai-backend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }