from typing import List

import pytest

from chat_pdf.services.answer_generator import AnswerGeneratorService


class FakeAnswerProvider:
    def __init__(self) -> None:
        self.calls: List[tuple[str, List[dict]]] = []

    def answer(self, question: str, context: List[dict]) -> str:
        self.calls.append((question, context))
        return "generated answer"


def test_answer_generator_service_returns_provider_answer() -> None:
    provider = FakeAnswerProvider()
    service = AnswerGeneratorService(provider)

    answer = service.answer("What is this?", [{"text": "context"}])

    assert answer == "generated answer"
    assert provider.calls == [("What is this?", [{"text": "context"}])]


def test_answer_generator_service_raises_for_empty_question() -> None:
    provider = FakeAnswerProvider()
    service = AnswerGeneratorService(provider)

    with pytest.raises(ValueError):
        service.answer("", [{"text": "context"}])
