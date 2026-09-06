import re

def normalize_text(text: str) -> str:
    """Normalize extracted document text without changing its meaning."""

    text = text.replace("\x00", "")
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Collapse repeated spaces while preserving line structure.
    text = re.sub(r"[ \t]+", " ", text)

    # Avoid excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()