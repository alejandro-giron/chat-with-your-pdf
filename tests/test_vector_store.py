from typing import List, Dict, Any

import pytest

from chat_pdf.services.vector_store import VectorStore, VectorStoreService


class FakeStore(VectorStore):
    def __init__(self) -> None:
        self.documents: List[Dict[str, Any]] = []

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        self.documents.extend(documents)

    def similarity_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        return [doc for doc in self.documents if query in doc.get("text", "")][:top_k]


def test_vector_store_service_adds_documents() -> None:
    store = FakeStore()
    service = VectorStoreService(store)

    service.add_documents([{"text": "hello", "embedding": [0.1]}])

    assert store.documents == [{"text": "hello", "embedding": [0.1]}]


def test_vector_store_service_returns_similar_documents() -> None:
    store = FakeStore()
    service = VectorStoreService(store)
    service.add_documents([
        {"text": "hello world", "embedding": [0.1]},
        {"text": "another topic", "embedding": [0.2]},
    ])

    results = service.similarity_search("hello", top_k=1)

    assert results == [{"text": "hello world", "embedding": [0.1]}]


def test_vector_store_service_raises_for_empty_query() -> None:
    store = FakeStore()
    service = VectorStoreService(store)

    with pytest.raises(ValueError):
        service.similarity_search("", top_k=1)
