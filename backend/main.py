"""
MedInsight AI FastAPI application entry point.
"""

from fastapi import FastAPI

from backend.routes.health import router as health_router
from backend.routes.reports import router as reports_router


app = FastAPI(
    title="MedInsight AI",
    description=(
        "AI-powered medical report understanding system. "
        "Provides informational analysis and does not provide "
        "medical diagnosis or treatment."
    ),
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(reports_router)


@app.get("/")
def root() -> dict[str, str]:
    """Return basic API information."""

    return {
        "name": "MedInsight AI",
        "version": "0.1.0",
        "status": "running",
    }