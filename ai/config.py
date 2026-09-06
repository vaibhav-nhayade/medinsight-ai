from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AIConfig:
    """Configuration for the MedInsight AI pipeline."""

    provider: str = os.getenv("LLM_PROVIDER", "")
    model: str = os.getenv("LLM_MODEL", "")
    api_key: str = os.getenv("LLM_API_KEY", "")

    temperature: float = 0.0
    max_output_tokens: int = 2000


config = AIConfig()