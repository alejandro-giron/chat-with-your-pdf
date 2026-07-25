from __future__ import annotations

from pathlib import Path


class PdfDocument:
    """Represents a local PDF file that can be indexed and queried."""

    def __init__(self, path: str | Path) -> None:
        resolved_path = Path(path).expanduser().resolve()

        if not resolved_path.exists():
            raise FileNotFoundError(f"PDF file does not exist: {resolved_path}")
        if not resolved_path.is_file():
            raise FileNotFoundError(f"PDF path is not a file: {resolved_path}")
        if resolved_path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a PDF file, got: {resolved_path}")

        self.path = resolved_path

    @property
    def name(self) -> str:
        return self.path.name
