from typing import List

from chat_pdf.services.ingestion_service import IngestionService


class FakeTextExtractor:
    def extract_text(self, document):
        return "alpha beta gamma"


class FakeChunker:
    def __init__(self) -> None:
        self.calls: List[str] = []

    def chunk(self, text: str):
        self.calls.append(text)
        return [text]


class FakeEmbeddingService:
    def __init__(self) -> None:
        self.calls: List[List[str]] = []

    def embed(self, texts: List[str]):
        self.calls.append(texts)
        return [[0.1, 0.2, 0.3] for _ in texts]


class FakeVectorStoreService:
    def __init__(self) -> None:
        self.documents: List[dict] = []

    def add_documents(self, documents: List[dict]) -> None:
        self.documents.extend(documents)


def test_ingestion_service_indexes_pdf_content() -> None:
    document = type("Document", (), {"name": "sample.pdf"})()
    text_extractor = FakeTextExtractor()
    chunker = FakeChunker()
    embedding_service = FakeEmbeddingService()
    vector_store = FakeVectorStoreService()

    service = IngestionService(
        text_extractor=text_extractor,
        chunker=chunker,
        embedding_service=embedding_service,
        vector_store_service=vector_store,
    )

    service.ingest(document)

    assert chunker.calls == ["alpha beta gamma"]
    assert embedding_service.calls == [["alpha beta gamma"]]
    assert len(vector_store.documents) == 1
    assert vector_store.documents[0]["text"] == "alpha beta gamma"
