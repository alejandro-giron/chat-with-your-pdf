from pathlib import Path
from typing import List

from chat_pdf.services.console_app import ConsoleApp


class FakeIngestionService:
    def __init__(self) -> None:
        self.documents: List[str] = []

    def ingest(self, document) -> None:
        self.documents.append(document.name)


class FakeQueryService:
    def __init__(self) -> None:
        self.questions: List[str] = []

    def query(self, question: str) -> str:
        self.questions.append(question)
        return "reply"


class FakeInput:
    def __init__(self, responses: List[str]) -> None:
        self._responses = responses

    def __call__(self, prompt: str) -> str:
        return self._responses.pop(0)


class FakeOutput:
    def __init__(self) -> None:
        self.lines: List[str] = []

    def write(self, message: str) -> None:
        self.lines.append(message)


class FailingIngestionService:
    def ingest(self, document) -> None:
        raise RuntimeError("Could not process PDF")


def test_console_app_runs_a_query_loop(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n")

    ingestion_service = FakeIngestionService()
    query_service = FakeQueryService()
    output = FakeOutput()
    app = ConsoleApp(
        ingestion_service=ingestion_service,
        query_service=query_service,
        input_func=FakeInput([str(pdf_path), "What is this?", ""]),
        output_func=output.write,
    )

    app.run()

    assert ingestion_service.documents == ["sample.pdf"]
    assert query_service.questions == ["What is this?"]
    assert any("reply" in line for line in output.lines)


def test_console_app_reports_ingestion_errors(tmp_path: Path) -> None:
    pdf_path = tmp_path / "broken.pdf"
    pdf_path.write_bytes(b"not a real pdf")

    output = FakeOutput()
    app = ConsoleApp(
        ingestion_service=FailingIngestionService(),
        query_service=FakeQueryService(),
        input_func=FakeInput([str(pdf_path)]),
        output_func=output.write,
    )

    app.run()

    assert any("Could not process PDF" in line for line in output.lines)
