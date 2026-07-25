from __future__ import annotations

import pdfplumber

from chat_pdf.domain.models import PdfDocument
from chat_pdf.interfaces.text_extractor import TextExtractor


class PdfPlumberTextExtractor(TextExtractor):
    """Extract text from a PDF document using pdfplumber."""

    def extract_text(self, document: PdfDocument) -> str:
        text_chunks: list[str] = []

        with pdfplumber.open(document.path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                if page_text:
                    text_chunks.append(page_text)

        return "\n".join(text_chunks).strip()
