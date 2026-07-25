from pathlib import Path

import pytest

from chat_pdf.domain.models import PdfDocument


def test_pdf_document_accepts_existing_file(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n")

    document = PdfDocument(pdf_path)

    assert document.path == pdf_path.resolve()
    assert document.name == "sample.pdf"


def test_pdf_document_rejects_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        PdfDocument(missing_path)
