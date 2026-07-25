from typing import List

import pytest

from chat_pdf.services.query_service import QueryService


class FakeVectorStoreService:
    def __init__(self, results: List[dict]) -> None:
        self.results = results

    def similarity_search(self, query: str, top_k: int = 3) -> List[dict]:
        return self.results[:top_k]


class FakeAnswerGenerator:
    def __init__(self) -> None:
        self.calls: List[tuple[str, List[dict]]] = []

    def answer(self, question: str, context: List[dict]) -> str:
        self.calls.append((question, context))
        return "answer"


def test_query_service_returns_answer_for_relevant_context() -> None:
    store = FakeVectorStoreService([{"text": "relevant context"}])
    generator = FakeAnswerGenerator()
    service = QueryService(store, generator)

    answer = service.query("What is this about?")

    assert answer == "answer"
    assert generator.calls[0][0] == "What is this about?"
    assert generator.calls[0][1] == [{"text": "relevant context"}]


def test_query_service_returns_fallback_when_no_context_found() -> None:
    store = FakeVectorStoreService([])
    generator = FakeAnswerGenerator()
    service = QueryService(store, generator)

    answer = service.query("What is this about?")

    assert answer == "I could not find relevant information in the document."
    assert generator.calls == []


def test_query_service_raises_for_empty_question() -> None:
    store = FakeVectorStoreService([])
    generator = FakeAnswerGenerator()
    service = QueryService(store, generator)

    with pytest.raises(ValueError):
        service.query("")
