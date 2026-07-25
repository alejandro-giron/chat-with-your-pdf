from pathlib import Path

import pytest

from chat_pdf.domain.models import PdfDocument
from chat_pdf.infrastructure.pdfplumber_text_extractor import PdfPlumberTextExtractor


MINIMAL_PDF_WITH_TEXT = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT /F1 18 Tf 72 72 Td (Hello world) Tj ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000062 00000 n 
0000000119 00000 n 
0000000206 00000 n 
0000000300 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
0
%%EOF
"""

MINIMAL_PDF_WITHOUT_TEXT = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 0 >>
stream
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000062 00000 n 
0000000119 00000 n 
0000000206 00000 n 
0000000300 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
0
%%EOF
"""


def test_extract_text_returns_text_from_pdf(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(MINIMAL_PDF_WITH_TEXT)
    document = PdfDocument(pdf_path)

    extractor = PdfPlumberTextExtractor()
    text = extractor.extract_text(document)

    assert "Hello world" in text


def test_extract_text_returns_empty_string_when_pdf_has_no_text(tmp_path: Path) -> None:
    pdf_path = tmp_path / "blank.pdf"
    pdf_path.write_bytes(MINIMAL_PDF_WITHOUT_TEXT)
    document = PdfDocument(pdf_path)

    extractor = PdfPlumberTextExtractor()
    text = extractor.extract_text(document)

    assert text == ""
