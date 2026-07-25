from __future__ import annotations

from typing import Callable, Optional

from chat_pdf.domain.models import PdfDocument


class ConsoleApp:
    """A simple console interface for ingesting a PDF and asking questions."""

    def __init__(
        self,
        ingestion_service,
        query_service,
        input_func: Optional[Callable[[str], str]] = None,
        output_func: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.ingestion_service = ingestion_service
        self.query_service = query_service
        self.input_func = input_func or input
        self.output_func = output_func or print

    def run(self) -> None:
        pdf_path = self.input_func("Enter the path to a PDF file: ").strip()
        if not pdf_path:
            self.output_func("No PDF path provided. Exiting.")
            return

        try:
            document = PdfDocument(pdf_path)
        except (FileNotFoundError, ValueError) as exc:
            self.output_func(str(exc))
            return

        try:
            self.ingestion_service.ingest(document)
        except Exception as exc:  # pragma: no cover - defensive handling for runtime failures
            self.output_func(str(exc))
            return

        self.output_func("Document indexed. You can now ask questions.")

        while True:
            question = self.input_func("Ask a question (blank to exit): ").strip()
            if not question:
                break

            answer = self.query_service.query(question)
            self.output_func(answer)
