from __future__ import annotations

from abc import ABC, abstractmethod

from chat_pdf.domain.models import PdfDocument


class TextExtractor(ABC):
    """Abstract interface for extracting text from a PDF document."""

    @abstractmethod
    def extract_text(self, document: PdfDocument) -> str:
        """Return the extracted text from the given PDF document."""
